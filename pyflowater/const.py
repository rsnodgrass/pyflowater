"""Constants used by PyFlo"""

FLO_USER_AGENT = 'PyFlo (pyflowater)'

FLO_V1_API_BASE = 'https://api.meetflo.com/api/v1'
FLO_V2_API_BASE = 'https://api-gw.meetflo.com/api/v2'

FLO_AUTH_URL       = FLO_V1_API_BASE + '/users/auth'
FLO_USERTOKENS_URL = FLO_V1_API_BASE + '/usertokens/me'

FLO_PRESENCE_HEARTBEAT = FLO_V2_API_BASE + '/presence/me'

# FIXME: for real time access to flow rates and
#https://firestore.googleapis.com/google.firestore.v1.Firestore/Listen/channel?database=projects%2Fflotechnologies-1b111%2Fdatabases%2F(default)&gsessionid={GSESSION_ID}&VER=8&RID=rpc&SID={SESSION_ID}&CI=0&AID=113&TYPE=xmlhttp&zx=lsvpgbg6aoar&t=2

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

INTERVAL_MINUTE='1m'
INTERVAL_HOURLY='1h'
INTERVAL_DAILY='1d'

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
