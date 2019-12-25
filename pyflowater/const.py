"""Constants used by PyFlo"""

FLO_USER_AGENT = 'PyFlo (https://github.com/rsnodgrass/pyflowater/)'

FLO_V1_API_PREFIX = 'https://api.meetflo.com/api/v1'
FLO_V2_API_PREFIX = 'https://api-gw.meetflo.com/api/v2'

FLO_AUTH_URL       = FLO_V1_API_PREFIX + '/users/auth'
FLO_USERTOKENS_URL = FLO_V1_API_PREFIX + '/usertokens/me'

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
