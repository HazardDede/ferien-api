"""Useful constants"""

import pytz

ALL_STATE_CODES = [
    "BW", "BY", "BE", "BB", "HB", "HH",
    "HE", "MV", "NI", "NW", "RP", "SL",
    "SN", "ST", "SH", "TH"
]

API_ALL_URL = 'https://ferien-api.de/api/v1/holidays'

API_STATE_URL = 'https://ferien-api.de/api/v1/holidays/{state_code}'

API_STATE_YEAR_URL = 'https://ferien-api.de/api/v1/holidays/' \
                     '{state_code}/{year}'

TZ_GERMANY = pytz.timezone("Europe/Berlin")
