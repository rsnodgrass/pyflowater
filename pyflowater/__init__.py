"""Base Python Class file for Flo"""

import json
import time
import logging
import requests

from pyflowater.const import ( FLO_USER_AGENT, FLO_V2_API_PREFIX, FLO_AUTH_URL )

LOG = logging.getLogger(__name__)

ACCESS_TOKEN_EXPIRY=30
REFRESH_TOKEN_EXPIRY=60

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

        self._auth_token = None

        # login the user
        self._username = username
        self._password = password
        self.login()

    def __repr__(self):
        """Object representation."""
        return "<{0}: {1}>".format(self.__class__.__name__, self.__username)

    def login(self):
        """Login to the Flo account and generate access token"""
        self.reset_headers()

        # authenticate with user/password
        payload = json.dumps({
            'username': self._username,
            'password': self._password
        })
        
        LOG.info("Authenticating Flo account %s via %s", self._username, FLO_AUTH_URL)
        response = requests.post(FLO_AUTH_URL, data=payload, headers=self._headers)
            # Example response:
            # { "token": "caJhb.....",
            #   "tokenPayload": { "user": { "user_id": "9aab2ced-c495-4884-ac52-b63f3008b6c7", "email": "your@email.com"},
            #                     "timestamp": 1559246133 },
            #   "tokenExpiration": 86400,
            #   "timeNow": 1559226161 }

        json_response = response.json()

        LOG.debug("Flo user %s authentication results %s : %s", self._username, FLO_AUTH_URL, json_response)
        self._auth_token_expiry = time.time() + int( int(json_response['tokenExpiration']) / 2)
        self._auth_token = json_response['token']
        self._user_id = json_response['tokenPayload']['user']['user_id']
        
    def _is_access_token_expired(self):
        return time.time() > self._auth_token_expiry

    @property
    def is_connected(self):
        """Connection status of client with Flo cloud service."""
        return bool(self._auth_token) and not self._is_access_token_expired()

    def reset_headers(self):
        """Reset the headers and params."""
        self._headers = {
            'User-Agent':    FLO_USER_AGENT,
            'Content-Type':  'application/json;charset=UTF-8',
            'Accept':        'application/json',
            'authorization':  self._auth_token
        }
        self.__params = {}

    def query(self, url, method='POST', extra_params=None, extra_headers=None, retry=3, force_login=True):
        """
        Returns a JSON object for an HTTP request.
        :param url: API URL
        :param method: Specify the method GET, POST or PUT (default=POST)
        :param extra_params: Dictionary to be appended on request.body
        :param extra_headers: Dictionary to be apppended on request.headers
        :param retry: Retry attempts for the query (default=3)
        """
        response = None
        self.reset_headers() # ensure the headers and params are reset to the bare minimum

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
            if method == 'GET':
                request = self._session.get(url, headers=headers)
            elif method == 'PUT':
                request = self._session.put(url, headers=headers, json=params)
            elif method == 'POST':
                request = self._session.post(url, headers=headers, json=params)
            else:
                LOG.error("Invalid request method '%s'", method)
                return None

            if request and (request.status_code == 200):
                response = request.json()
                break # success!

        return response

    @property
    def locations(self):
        """Return all locations registered with the Flo account."""
        # https://api-gw.meetflo.com/api/v2/users/<userId>?expand=locations
        url = f"{FLO_V2_API_PREFIX}/users/{self._user_id}?expand=locations"
        return self.query(url, method='GET')

    @property
    def devices(self, locationId):
        """Return all devices at a location"""
        url = f"{FLO_V2_API_PREFIX}/locations/{locationId}?expand=devices"
        return self.query(url, method='GET')

    @property
    def run_health_test(self, deviceId):
        url = f"{FLO_V2_API_PREFIX}/devices/{deviceId}/healthTest/run"
        return self.query(url, method='POST')

    @property
    def alerts(self, locationId):
        """Return all devices at a location"""
        params = { 'isInternalAlarm': 'false',
                   'locationId': locationId,
                   'status': 'triggered',
                   'severity': 'warning',
                   'severity': 'critical',
                   'page': 1,
                   'size': 100
        }
        url = f"{FLO_V2_API_PREFIX}/alerts"
        return self.query(url, method='GET', extra_params=params)

    @property
    def consumption(self, locationId):
        """Return consumption for a location"""
        params = { 'locationId': locationId,
                   'startDate': '2019-12-24T08:00:00.000Z',
                   'endDate': '2019-12-25T07:59:59.999Z',
                   'interval': '1h'
        }
        url = f"{FLO_V2_API_PREFIX}/water/consumption"
        return self.query(url, method='GET', extra_params=params)
