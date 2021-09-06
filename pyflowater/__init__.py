"""Base Python Class file for Flo"""

import json
import time
import logging
from datetime import timezone, datetime
import requests

from pyflowater.flostream import FloListener
from pyflowater.const import (
    FLO_USER_AGENT,
    FLO_V2_API_BASE,
    FLO_AUTH_URL,
    FLO_MODES,
    FLO_TIME_FORMAT,
    FLO_PRESENCE_HEARTBEAT,
    INTERVAL_HOURLY,
    INTERVAL_DAILY,
    INTERVAL_MONTHLY
)

LOG = logging.getLogger(__name__)

METHOD_GET = 'GET'
METHOD_PUT = 'PUT'
METHOD_POST = 'POST'

DEVICE_ID_TO_LOCATION_MAC_TUPLE = {}


class FloError(Exception):
    pass


class PyFlo:
    """Base object for Flo."""

    def __init__(self, username, password=None):
        """Create a PyFlo object.
        :param username: Flo user email
        :param password: Flo user password
        :returns PyFlo base object
        """
        self._session = requests.Session()
        self._headers = {}
        self.clear_cache()

        self._auth_token = None
        self._username = username
        self._password = None # call save_password() if you want to save it

        self.login_with_password(password)

    def __repr__(self):
        """Object representation."""
        return "<{0}: {1}>".format(self.__class__.__name__, self._username)
    
    def login(self):
        if self._password:
            self.login_with_password(self._password)

    def save_password(self, password):
        """Client can save password to enable automatic reauthentication"""
        self._password = password

    def login_with_password(self, password):
        """Login to the Flo account and generate access token"""
        self._reset_headers()

        # authenticate with user/password
        payload = json.dumps({
            'username': self._username,
            'password': password
        })
        
        LOG.debug(f"Authenticating Flo account {self._username} via {FLO_AUTH_URL}")
        response = requests.post(FLO_AUTH_URL, data=payload, headers=self._headers)
            # Example response:
            # { "token": "caJhb.....",
            #   "tokenPayload": { "user": { "user_id": "9aab2ced-c495-4884-ac52-b63f3008b6c7", "email": "your@email.com"},
            #                     "timestamp": 1559246133 },
            #   "tokenExpiration": 86400,
            #   "timeNow": 1559226161 }

        json_response = response.json()
        #LOG.debug("Flo user %s authentication results %s : %s", self._username, FLO_AUTH_URL, json_response)

        if 'token' in json_response:
            self._auth_token = json_response['token']
            self._auth_token_expiry = time.time() + int( int(json_response['tokenExpiration']) / 2)
            self._user_id = json_response['tokenPayload']['user']['user_id']
        else:
            LOG.error(f"Failed authenticating Flo user {self._username}")

    @property
    def is_connected(self):
        """Connection status of client with Flo cloud service."""
        return bool(self._auth_token) and time.time() < self._auth_token_expiry

    @property
    def user_id(self):
        return self._user_id

    def _reset_headers(self):
        """Reset the headers and params."""
        self._headers = {
            'User-Agent':    FLO_USER_AGENT,
            'Content-Type':  'application/json;charset=UTF-8',
            'Accept':        'application/json',
            'authorization':  self._auth_token
        }
        self.__params = {}

    def query(self, url, method=METHOD_POST, extra_params=None, extra_headers=None, retry=3, force_login=True):
        """
        Returns a JSON object for an HTTP request (no caching included)
        :param url: API URL
        :param method: Specify the method GET, POST or PUT (default=POST)
        :param extra_params: Dictionary to be appended on request.body
        :param extra_headers: Dictionary to be apppended on request.headers
        :param retry: Retry attempts for the query (default=3)
        """
        response = None
        self._reset_headers() # ensure the headers and params are reset to the bare minimum

        if force_login and not self.is_connected:
            self.login()

        loop = 0
        while loop <= retry:
            loop += 1

            # override request.body or request.headers dictionary
            params = {}
            if extra_params:
                params.update(extra_params)

            headers = self._headers
            if extra_headers:
                headers.update(extra_headers)

            LOG.debug("Query: %s %s (attempt %s/%s)", method, url, loop, retry)
            LOG.debug("... Params: %s", params)
            LOG.debug("... Headers: %s", headers)

            # define connection method
            response = None
            if method == METHOD_GET:
                response = self._session.get(url, headers=headers, params=extra_params)
            elif method == METHOD_PUT:
                response = self._session.put(url, headers=headers, json=params)
            elif method == METHOD_POST:
                response = self._session.post(url, headers=headers, json=params)
            else:
                LOG.error(f"Invalid request method: {method}")
                return None

            if response.status_code == 200:
                json = response.json() 
                LOG.debug(f"Received from {method} {url}: %s", json)
                return json
            else:
                LOG.debug(f"Received from {method} {url} code {response.status_code}: %s", response)

        return None

    def clear_cache(self):
        self._cached_data = None
        self._cached_locations = {}

    def data(self, use_cached=True):
        if not self._cached_data or use_cached == False:
            # https://api-gw.meetflo.com/api/v2/users/<userId>?expand=locations
            url = f"{FLO_V2_API_BASE}/users/{self._user_id}?expand=locations"
            self._cached_data = self.query(url, method='GET')
        return self._cached_data


    def alarms(self, use_cached=False):
        """Get all alarms for the Flo account"""
        url = f"{FLO_V2_API_BASE}/alarms"
        data = self.query(url, method=METHOD_GET)
        return data.json()
    
    def locations(self, use_cached=True):
        """Return all locations registered with the Flo account."""
        data = self.data(use_cached=use_cached)
        return data['locations']

    def location(self, location_id, use_cached=True):
        """Return details on all devices at a location"""
        # NOTE: since we always expand locations on the overall data, we could skip this call
        if not location_id in self._cached_locations or use_cached == False:
            url = f"{FLO_V2_API_BASE}/locations/{location_id}?expand=devices"
            data = self.query(url, method=METHOD_GET)
            if not data:
                LOG.warning(f"Failed to load data from {url}")
                return None
            self._cached_locations[location_id] = data
        
        if location_id in self._cached_locations:
            return self._cached_locations[location_id]
        else:
            return None

    def run_health_test(self, device_id):
        """Run the health test for the specified Flo device"""
        url = f"{FLO_V2_API_BASE}/devices/{device_id}/healthTest/run"
        return self.query(url, method=METHOD_POST)

    def device(self, device_id):
        url = f"{FLO_V2_API_BASE}/devices/{device_id}"
        data = self.query(url, method=METHOD_GET)
        return data

    def preset_mode(self, device_id):
        data = self.device(device_id)
        systemMode = data['systemMode']
        return systemMode['target']

    def telemetry(self, device_id):
        data = self.device(device_id)
        telemetry = data['telemetry']
        return telemetry['current']

    def valve_status(self, device_id):
        data = self.device(device_id)
        valve = data['valve']
        return valve['lastKnown']

    def open_valve(self, device_id):
        LOG.debug(f"Opening valve for device {device_id}")
        url = f"{FLO_V2_API_BASE}/devices/{device_id}"
        self.query(url, extra_params={ "valve": { "target": "open" }}, method=METHOD_POST)

    def close_valve(self, device_id):
        LOG.debug(f"Closing valve for device {device_id}")
        url = f"{FLO_V2_API_BASE}/devices/{device_id}"
        self.query(url, extra_params={ "valve": { "target": "closed" }}, method=METHOD_POST)

    def set_mode(self, location_id: str, mode: str, additional_params={}):
        url = f"{FLO_V2_API_BASE}/locations/{location_id}/systemMode"

        params = {"target": mode}
        if mode == "sleep":
            # Number of minutes to sleep (120=2 hours, 480=8 hours)
            params["revertMinutes"] = 480
            # Mode to set after sleep concludes ("away" or "home")
            params["revertMode"] = 'home'

        if additional_params:
            params = {**params, **additional_params}
        self.query(url, extra_params=params, method=METHOD_POST)
              
    def alerts(self, location_id):
        """Return alerts for a location"""

        params = { 'isInternalAlarm': 'false',
                   'locationId': location_id,
                   'status': 'triggered',
                   'severity': 'warning',
                   'severity': 'critical',
                   'page': 1,
                   'size': 100
        }
        url = f"{FLO_V2_API_BASE}/alerts"
        return self.query(url, method='GET', extra_params=params)

    def _get_locid_mac(self, device_id):
        """Find the location_id and MAC address for device_id"""
        for location in self.locations():
            for device in location['devices']:
                if device['id'] == device_id:
                    return (location['id'], device['macAddress'])
        raise FloError(f'no device with id {device_id}')

    def consumption(self, device_id, startDate=None, endDate=None, interval=INTERVAL_HOURLY):
        """Return consumption data for a given device id. If startDate or endDate are naive
        (tzinfo is None), they are assumed to represent local time of the running system."""

        (location_id, mac_address) = self._get_locid_mac(device_id)

        # calculate since beginning of day in LOCAL timezone
        now = datetime.now()
        if not startDate:
            startDate = now.replace(hour=0, minute=0, second=0, microsecond=0)

        if not endDate:
            # Flo website queries for current data sets end timestamp as the last millisecond of the day, so do the same
            endDate = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        # in a python 3.6-or-later world we could use startDate_utc = startDate.astimezone(timezone.utc).
        # note that fromtimestamp(timestamp()) only works for times supported by the system gmtime().
        # see https://docs.python.org/3/library/datetime.html#datetime.datetime.fromtimestamp
        startDate_utc = datetime.fromtimestamp(startDate.timestamp(), timezone.utc)
        endDate_utc = datetime.fromtimestamp(endDate.timestamp(), timezone.utc)

        # in python 3.6 and later, consider startDate.isoformat(timespec='milliseconds')
        params = { 'locationId': location_id,
                   'macAddress': mac_address,
                   'startDate': startDate_utc.strftime(FLO_TIME_FORMAT) + 'Z',
                   'endDate': endDate_utc.strftime(FLO_TIME_FORMAT) + 'Z',
                   'interval': interval,
        }
        
        url = f"{FLO_V2_API_BASE}/water/consumption"
        return self.query(url, method=METHOD_GET, extra_params=params)

    def get_real_time_listener(self, device_id, callback, heartbeat=True):
        """Begin listening for the specified device, sending results to the specified callback.

        Callback is a function that accepts a single argument containing the dictionary returned by the Flo service, of the form:

  {
    "valve": { "lastKnown": "open" },
    "systemMode": { "lastKnown": "home" },
    "telemetry": { "current": { "psi": 51.1, "updated": "2021-09-04T23:07:03Z", "gpm": 0.0, "tempF": 68.4 } },
    ...
  }

        If heartbeat is True (the default), we spawn a thread to tell the device
        to stream telemetry into firestore. If heartbeat is False, we don't.
        Streaming telemetry (especially in the inefficient way Flo does it) is
        costly, so please don't do this willy-nilly or they will shut us off.

        Returns a FloListener. You must call start() on the returned
        instance to begin receiving callbacks.

        """
        # we issue one heartbeat initially even if we won't issue any later,
        # since presumably we want one callback with the current data.
        self._do_heartbeat()
        url = f"{FLO_V2_API_BASE}/session/firestore"
        data = self.query(url, method=METHOD_POST)
        (location_id, mac_address) = self._get_locid_mac(device_id)
        return FloListener(
            heartbeat and self._do_heartbeat, data['token'], mac_address, callback
        )

    def _do_heartbeat(self):
        self.query(FLO_PRESENCE_HEARTBEAT, method=METHOD_POST)
