"""Base Python Class file for Flo"""

import json
import time
import logging
import requests

from pyflowater.const import ( FLO_USER_AGENT, FLO_V2_API_PREFIX, FLO_AUTH_URL, FLO_MODES )

LOG = logging.getLogger(__name__)

METHOD_GET = 'GET'
METHOD_PUT = 'PUT'
METHOD_POST = 'POST'

class PyFlo(object):
    """Base object for SensorPush."""

    def __init__(self, username=None, password=None):
        """Create a PyFlo object.
        :param username: Flo user email
        :param password: Flo user password
        :returns PyFlo base object
        """
        self._session = requests.Session()
        self._headers = {}
        self._params = {}
        self.clear_cache()

        self._auth_token = None
        self._username = username
        self._password = password
        self.login()

    def __repr__(self):
        """Object representation."""
        return "<{0}: {1}>".format(self.__class__.__name__, self._username)

    def login(self):
        """Login to the Flo account and generate access token"""
        self._reset_headers()

        # authenticate with user/password
        payload = json.dumps({
            'username': self._username,
            'password': self._password
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

        # FIXME: this should really use refresh token, if possible, to reauthenticate
        if force_login and not self.is_connected:
            self.login()

        loop = 0
        while loop <= retry:

            # override request.body or request.headers dictionary
            params = self._params
            if extra_params:
                params.update(extra_params)
            LOG.debug("Params: %s", params)

            headers = self._headers
            if extra_headers:
                headers.update(extra_headers)
            LOG.debug("Headers: %s", headers)

            loop += 1
            LOG.debug("Querying %s on attempt: %s/%s", url, loop, retry)

            # define connection method
            request = None
            if method == METHOD_GET:
                request = self._session.get(url, headers=headers)
            elif method == METHOD_PUT:
                request = self._session.put(url, headers=headers, json=params)
            elif method == METHOD_POST:
                request = self._session.post(url, headers=headers, json=params)
            else:
                LOG.error("Invalid request method '%s'", method)
                return None

            if request and (request.status_code == 200):
                response = request.json()
                break # success!

        return response

    def clear_cache(self):
        self._cached_data = None
        self._cached_locations = {}

    def data(self, use_cached=True):
        if not self._cached_data or use_cached == False:
            # https://api-gw.meetflo.com/api/v2/users/<userId>?expand=locations
            url = f"{FLO_V2_API_PREFIX}/users/{self._user_id}?expand=locations"
            self._cached_data = self.query(url, method='GET')
        return self._cached_data

    def locations(self, use_cached=True):
        """Return all locations registered with the Flo account."""
        data = self.data(use_cached=use_cached)
        return data['locations']

    def location(self, location_id, use_cached=True):
        """Return details on all devices at a location"""
        # NOTE: since we always expand locations on the overall data, we could skip this call
        if not location_id in self._cached_locations or use_cached == False:
            url = f"{FLO_V2_API_PREFIX}/locations/{location_id}?expand=devices"
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
        url = f"{FLO_V2_API_PREFIX}/devices/{device_id}/healthTest/run"
        return self.query(url, method=METHOD_POST)

    def device(self, device_id):
        url = f"{FLO_V2_API_PREFIX}/devices/{device_id}"
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

    def turn_valve_on(self, device_id):
        url = f"{FLO_V2_API_PREFIX}/devices/{device_id}"
        self.query(url, extra_params={ "valve": { "target": "open" }})

    def turn_valve_off(self, device_id):
        url = f"{FLO_V2_API_PREFIX}/devices/{device_id}"
        self.query(url, extra_params={ "valve": { "target": "closed" }})

    def set_preset_mode(self, device_id, mode):
        """Run the health test for the specified Flo device"""
        if not mode in FLO_MODES:
            LOG.error(f"Invalid preset mode {mode} (must be {FLO_MODES})")
            return

        url = f"{FLO_V2_API_PREFIX}/devices/{device_id}"
        return self.query(url, method=METHOD_POST, extra_params={ "systemMode": { "target": mode }})

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
        url = f"{FLO_V2_API_PREFIX}/alerts"
        return self.query(url, method='GET', extra_params=params)

    def consumption(self, location_id, startDate=None, endDate=None, interval='1h'):
        """Return consumption for a location"""

        if not startDate:
            startDate = '2019-12-24T08:00:00.000Z' # FIXME: calculate for start of today

        if not endDate:
            startDate = '2019-12-25T07:59:59.999Z' # FIXME: calculate for end of startDate

        params = { 'locationId': location_id,
                   'startDate': startDate,
                   'endDate': endDate,
                   'interval': interval
        }
        url = f"{FLO_V2_API_PREFIX}/water/consumption"
        LOG.info(f"Loading {url}")
        return self.query(url, method=METHOD_GET, extra_params=params)
