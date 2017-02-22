import os


## SITES - Set to True/False if you want them scraped

CRAIGSLIST = True
KIJIJI = True

## Price Filters

# The minimum rent you want to pay per month.
MIN_PRICE = 500

# The maximum rent you want to pay per month.
MAX_PRICE = 1900

#
HAS_IMAGE = 1

#postal code
POSTAL = 'M5J1E6'

#distance
SEARCH_DISTANCE = 5


## Craigslist slack posting fields
SLACK_PARAMS = {
    'craigslist': {
        'post_fields': {
            'price' : 'Price: ',
            'metro_dist': 'Distance to Subway (km): ',
            'area': 'Neighborhood: ',
            'where': 'Address: ',
            'metro': 'Nearest Subway: ',
            'meta': 'Extra Info: '
            },
        'channel': 'craigslist'
    },
    'kijiji': {
        'post_fields': {
            'price' : 'Price: ',
            'address': 'Address: ',
            'metro_dist': 'Distance to Subway (km): ',
            'area': 'Neighborhood: ',
            'metro': 'Nearest Subway: '
            },
        'channel': 'kijiji'
    }
}

## Location preferences

# The Craigslist site you want to search on.
# For instance, https://sfbay.craigslist.org is SF and the Bay Area.
# You only need the beginning of the URL.
CRAIGSLIST_SITE = 'toronto'

# What Craigslist subdirectories to search on.
# For instance, https://sfbay.craigslist.org/eby/ is the East Bay, and https://sfbay.craigslist.org/sfc/ is San Francisco.
# You only need the last three letters of the URLs.
AREAS = ["tor"]

# A list of neighborhoods and coordinates that you want to look for apartments in.  Any listing that has coordinates
# attached will be checked to see which area it is in.  If there's a match, it will be annotated with the area
# name.  If no match, the neighborhood field, which is a string, will be checked to see if it matches
# anything in NEIGHBORHOODS.
BOXES = [
    ("distillery", [
        [43.646914, -79.352102],
        [43.658886,	-79.367383],
    ]),
    ("downtown-core", [
        [43.637597, -79.369183],
        [43.658055, -79.393217],
    ]),
    ("downtown-central", [
        [43.653807, -79.381885],
        [43.669574, -79.403172],
    ]),
    ("mid-west", [
        [43.64946, -79.396048],
        [43.667965, -79.459906],
    ]),
    ("south-west", [
        [43.640951, -79.3824],
        [43.652867, -79.407291],
    ]),
    ('all', [
        [43.626943, -79.352875],
        [43.663712, -79.439907],
    ])
]

# A list of neighborhood names to look for in the Craigslist neighborhood name field. If a listing doesn't fall into
# one of the boxes you defined, it will be checked to see if the neighborhood name it was listed under matches one
# of these.  This is less accurate than the boxes, because it relies on the owner to set the right neighborhood,
# but it also catches listings that don't have coordinates (many listings are missing this info).
NEIGHBORHOODS = ['Yonge','Bloor','Queen','King','Toronto','Downtown','Liberty','Spadina','College']

## Transit preferences

# The farthest you want to live from a transit stop.
MAX_TRANSIT_DIST = 4 # kilometers

# Transit stations you want to check against.  Every coordinate here will be checked against each listing,
# and the closest station name will be added to the result and posted into Slack.
TRANSIT_STATIONS = {
    "st_andrew": [43.647400, -79.384358],
    "osgoode": [43.650754, -79.386718],
    "union": [43.645599, -79.380367],
    "king": [43.648674, -79.377835],
    "queen": [43.652307, -79.379208],
    "college": [43.6613247, -79.3852633],
    "dundas": [43.6552859,-79.3797379],
    "st_patrick": [43.6538735,-79.3832671],
    "queens_park": [43.6538735,-79.3832671],
    "museum": [43.663281,-79.3969142],
    "spadina": [43.663281,-79.3969142],
    "st_george": [43.663281,-79.3969142],
    "wellesley": [43.663281,-79.3969142],
    "bloor_yonge": [43.663281,-79.3969142],
    "bay": [43.6634052,-79.3968713],
    'dupont': [43.6670063,-79.4074714],
    'bathurst': [43.6629395,-79.4161832],
    'christie': [43.6629395,-79.4161832],
    'ossington': [43.6603316,-79.4264829],
    'dufferin': [43.6582514,-79.4377267]
}

## Search type preferences

# The Craigslist section underneath housing that you want to search in.
# For instance, https://sfbay.craigslist.org/search/apa find apartments for rent.
# https://sfbay.craigslist.org/search/sub finds sublets.
# You only need the last 3 letters of the URLs.
CRAIGSLIST_HOUSING_SECTION = 'apa'

## System settings

# How long we should sleep between scrapes of Craigslist.
# Too fast may get rate limited.
# Too slow may miss listings.
SLEEP_INTERVAL = 1 * 60 # 20 minutes


# The token that allows us to connect to slack.
# Should be put in private.py, or set as an environment variable.

#Any private settings are imported here.
#slack token in private.py
try:
    from private import *
except ImportError:
    try:
        from src.private import *
    except:
        pass
except Exception:
    pass


# Any external private settings are imported from here.
try:
    from config.private import *
except Exception:
    pass
