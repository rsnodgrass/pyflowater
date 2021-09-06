"""Code relating to the firestore API Flo use to stream live data."""

import requests
import json
import threading
from google.cloud import firestore
from google.oauth2.credentials import Credentials

from pyflowater.const import (
    FLO_GOOGLE_API_KEY,
    FIREBASE_REST_API,
    FLO_FIRESTORE_PROJECT,
    FLO_HEARTBEAT_DELAY,
)

def _get_token_info(token):
    url = f"{FIREBASE_REST_API}/verifyCustomToken?key={FLO_GOOGLE_API_KEY}"
    headers = {"Content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"returnSecureToken": True, "token": token})
    resp = requests.post(url, headers=headers, data=data)
    return resp.json()


class FloListener:
    """Flo firestore listener class."""

    def __init__(self, heartbeat, token, deviceId, callback):
        self._heartbeat_func = heartbeat
        self._token = token
        self._deviceId = deviceId
        self._callback = callback
        self._watch = None
        self._client = None
        self._doc_ref = None

    def set_callback(self, callback):
        """Update the callback."""
        self._callback = callback

    def start(self):
        """Begin listening on the firestore database.

        Note that this will immediately cause firestore to respond with the current state of the device, which incurs server-side costs.
        Because of this, only stop() again once you're not expecting to need any further updates (e.g. don't start/stop on a whim)."""
        if self._watch:
            return
        if not self._client:
            tinfo = _get_token_info(self._token)
            creds = Credentials(tinfo['idToken'], refresh_token=tinfo['refreshToken'])
            self._client = firestore.Client(project=FLO_FIRESTORE_PROJECT, credentials=creds)
        if not self._doc_ref:
            self._doc_ref = self._client.collection('devices').document(self._deviceId)
        self._watch = self._doc_ref.on_snapshot(self._handle)
        if self._heartbeat_func:
            self._heartbeat = threading.Timer(FLO_HEARTBEAT_DELAY, self._do_heartbeat)
            self._heartbeat.start()
        else:
            self._heartbeat = None

    def stop(self):
        """Shut down the listener, if started."""
        if not self._watch:
            return
        self._watch.close()
        self._watch = None
        if self._heartbeat:
            self._heartbeat.cancel()
            self._heartbeat = None

    def _handle(self, document, changes, timestamp):
        self._callback(document[0].to_dict())

    def _do_heartbeat(self):
        if not self._watch:
            # Thread started before stop() was called, so bail out now
            return
        self._heartbeat_func()
        self._heartbeat = threading.Timer(FLO_HEARTBEAT_DELAY, self._do_heartbeat)
        self._heartbeat.start()
