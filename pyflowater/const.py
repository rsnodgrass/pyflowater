"""Constants used by PyFlo"""

FLO_USER_AGENT = 'PyFlo (pyflowater)'

FLO_V1_API_BASE = 'https://api.meetflo.com/api/v1'
FLO_V2_API_BASE = 'https://api-gw.meetflo.com/api/v2'

FLO_AUTH_URL       = FLO_V1_API_BASE + '/users/auth'
FLO_USERTOKENS_URL = FLO_V1_API_BASE + '/usertokens/me'

FLO_PRESENCE_HEARTBEAT = FLO_V2_API_BASE + '/presence/me'
FLO_HEARTBEAT_DELAY = 60.0  # their timeout appears to be 2 minutes, so half that

"""
V1 APIs

- https://api.meetflo.com/api/v1/usertokens/me
- https://api.meetflo.com/api/v1/icds/me
- https://api.meetflo.com/api/v1/alerts/icd/{flo_icd_id}?size=1
- https://api.meetflo.com/api/v1/alerts/icd/{flo_icd_id}?page=1&size=10
- https://api.meetflo.com/api/v1/locations/me
- https://api.meetflo.com/api/v1/users/me
- https://api.meetflo.com/api/v1/userdetails/me
"""

FLO_HOME = 'home'
FLO_AWAY = 'away'
FLO_SLEEP = 'sleep'
FLO_MODES = [ FLO_HOME, FLO_AWAY, FLO_SLEEP ]

FLO_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.000' # Flo required format is 2020-04-11T08:00:00.000Z

FIREBASE_REST_API = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty'
FLO_GOOGLE_API_KEY = 'AIzaSyBBquh94zXF15FORbe2lJC9J8kerqsVo9Y'
FLO_FIRESTORE_PROJECT = 'flotechnologies-1b111'

INTERVAL_HOURLY='1h'
INTERVAL_DAILY='1d'
INTERVAL_MONTHLY='1m'

FLO_UNIT_SYSTEMS = {
    'imperial_us': { 
        'system':   'imperial_us',
        'temp':     '°F',
        'flow':     'gpm',
        'pressure': 'psi',
    },
    'imperial_uk': { 
        'system':   'imperial_uk',
        'temp':     '°F',
        'flow':     'gpm',
        'pressure': 'psi',
    },
    'metric': { 
        'system':   'metric',
        'temp':     '°C',
        'flow':     'lpm',
        'pressure': 'kPa'
    }
}
