"""Code relating to the firestore API Flo use to stream live data."""

import requests
import json
from google.cloud import firestore
from google.oauth2.credentials import Credentials

from pyflowater.const import (
    FLO_GOOGLE_API_KEY,
    FIREBASE_REST_API,
    FLO_FIRESTORE_PROJECT,
)

def _get_token_info(token):
    url = f"{FIREBASE_REST_API}/verifyCustomToken?key={FLO_GOOGLE_API_KEY}"
    headers = {"Content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"returnSecureToken": True, "token": token})
    resp = requests.post(url, headers=headers, data=data)
    return resp.json()

class FloListener:
    """Flo firestore listener class."""

    def __init__(self, token, deviceId, callback):
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
        """Begin listening on the firestore database."""
        if self._watch:
            return
        if not self._client:
            tinfo = _get_token_info(self._token)
            creds = Credentials(tinfo['idToken'], refresh_token=tinfo['refreshToken'])
            self._client = firestore.Client(project=FLO_FIRESTORE_PROJECT, credentials=creds)
        if not self._doc_ref:
            self._doc_ref = self._client.collection('devices').document(self._deviceId)
        self._watch = self._doc_ref.on_snapshot(self._handle)

    def stop(self):
        """Shut down the listener, if started."""
        if not self._watch:
            return
        self._watch.close()
        self._watch = None

    def _handle(self, document, changes, timestamp):
        self._callback(document[0].to_dict())
