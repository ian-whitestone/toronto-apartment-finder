import os

LOG_PATH = 'logs'

####################
### TESTING MODE ###
####################

# Toggle testing to true/false for testing mode
TESTING = False
TESTING_CHANNEL = 'testing'


#########################
### FEATURES TOGGLING ###
#########################

# SITES - Set to True/False if you want them scraped
CRAIGSLIST = True
KIJIJI = True

# True if you would like posts with the image preview, and other parameters
# False if you would prefer simple posts with default description & url
ENHANCED_POSTS = True

######################
### SEARCH FILTERS ###
######################

# The minimum rent you want to pay per month.
MIN_PRICE = 500

# The maximum rent you want to pay per month.
MAX_PRICE = 1900

# Kijiji/Craiglist image requirement: 0 or 1
HAS_IMAGE = 1

#postal code to search within
POSTAL = 'M5J1E6'

#distance
SEARCH_DISTANCE = 5



#######################
### SLACK CONSTANTS ###
#######################

# Name of your slack bot
SLACK_BOT = 'toby'

# For each site, map the key name from the scraping result to the description
# you would like to appear in the slack post
SLACK_PARAMS = {
    'craigslist': {
        'price' : 'Price: ',
        'metro_dist': 'Subway (km): ',
        'area': 'Neighborhood: ',
        'where': 'Address: ',
        'metro': 'Nearest Subway: ',
        'meta': 'Extra Info: '
    },
    'kijiji': {
        'price' : 'Price: ',
        'address': 'Address: ',
        'metro_dist': 'Subway (km): ',
        'area': 'Neighborhood: ',
        'metro': 'Nearest Subway: '
    }
}


# enter the parameters you would like to have colour coded
# there are two types of colour coding methodologies
# 1) "range" will check if the parameter value falls within specified range
# 2) "list" will check if the parameter value falls within a specified list
# 3 standard colours - good is green, warning is yellow, danger is red.
# feel free to swap those out with any hex colour code
COLOURS = {
    'price': {
        'levels': {
            'good': [0, 1500],
            'warning': [1501, 1700],
            'danger': [1701,10000]
        },
        'type': "range"
    },
    'metro_dist': {
        'levels': {
            'good': [0, 0.75],
            'warning': [0.76, 1.5],
            'danger': [1.51,10]
        },
        'type': "range"
    },
    'area': {
        'levels': {
            'good': ['st-lawrence', 'queen-west', 'liberty-village',
                'ossington', 'Queen', 'King', 'Liberty'],
            'warning': ['distillery','financial-district', 'mid-west',
                'Spadina', 'College', 'Downtown'],
            'danger': ['yonge-corridor','bloor-west', 'Yonge',
                'Bloor', 'Toronto']
        },
        'type': "list"
    }
}

# for the parameters which will be colour coded as defined in COLOURS,
# enter the order you would like them displayed in so the messages are
# consistently formatted
COLOUR_PARAM_ORDER = ['price', 'area', 'metro_dist']


# map each neighborhood to the slack channel you would like it posted in

SLACK_CHANNELS = {
    'st-lawrence': 'south-east',
    'distillery': 'south-east',
    'queen-west': 'queen-west',
    'Queen': 'queen-west',
    'liberty-village': 'liberty-village',
    'Liberty': 'liberty-village',
    'ossington': 'liberty-village',
    'Downtown': 'downtown',
    'financial-district': 'downtown',
    'yonge-corridor': 'downtown',
    'Yonge': 'downtown',
    'King': 'downtown',
    'mid-west': 'mid-west',
    'bloor-west': 'mid-west',
    'Bloor': 'mid-west',
    'Toronto': 'mid-west',
    'College': 'mid-west',
    'Spadina': 'mid-west'
}

# default channel for listings to be posted to
DEFAULT_CHANNEL = 'mid-west'

# default colour for slack messages
DEFAULT_COLOUR = '#524e4d'

# This is the order in which the parameters will be posted
# For ex., defaults will be posted first, followed by any fields with a 'good' rating
COLOUR_ORDER = [DEFAULT_COLOUR, 'good', 'warning', 'danger']




###########################
### CRAIGSLIST SETTINGS ###
###########################

# The Craigslist site you want to search on.
# For instance, https://sfbay.craigslist.org is SF and the Bay Area.
# You only need the beginning of the URL.
CRAIGSLIST_SITE = 'toronto'

# What Craigslist subdirectories to search on.
# For instance, https://sfbay.craigslist.org/eby/ is the East Bay, and https://sfbay.craigslist.org/sfc/ is San Francisco.
# You only need the last three letters of the URLs.
AREAS = ["tor"]


# The Craigslist section underneath housing that you want to search in.
# For instance, https://sfbay.craigslist.org/search/apa find apartments for rent.
# https://sfbay.craigslist.org/search/sub finds sublets.
# You only need the last 3 letters of the URLs.
CRAIGSLIST_HOUSING_SECTION = 'apa'

#######################
### KIJIJI SETTINGS ###
#######################

UNIT_TYPE_MAP = {
    'studio': 'b-bachelor-studio',
    '1bed': 'b-1-bedroom',
    '1bed_den': 'b-1-bedroom-den',
    'all': 'b-apartments-condos',
    'house': 'b-house-rental'
    }

# enter the types of units you would like to parse
# 'all' includes studios, 1beds, 1beds + den
# 'all' DOES NOT INCLUDE houses
UNIT_TYPES = ['all', 'house']

# 0 if you want un-furnished units, 1 for furnished units
FURNISHED = 0



############################
### LOCATION PREFERENCES ###
############################

# A list of neighborhoods and coordinates that you want to look for apartments in.  Any listing that has coordinates
# attached will be checked to see which area it is in.  If there's a match, it will be annotated with the area
# name.  If no match, the neighborhood field, which is a string, will be checked to see if it matches
# anything in NEIGHBORHOODS.
BOXES = [
    ("distillery", [
        [43.650516, -79.35236],
        [43.655841,	-79.370513],
    ]),
    ("st-lawrence", [
        [43.644507, -79.370513],
        [43.655841, -79.376349],
    ]),
    ("financial-district", [
        [43.644662, -79.376521],
        [43.649879, -79.387422],
    ]),
    ("yonge-corridor", [
        [43.649879, -79.383602],
        [43.670557, -79.387422],
    ]),
    ("mid-west", [
        [43.650516, -79.389224],
        [43.669222, -79.412184],
    ]),
    ("mid-west", [
        [43.649321, -79.394953],
        [43.663867, -79.417913],
    ]),
    ("queen-west", [
        [43.643855, -79.384825],
        [43.65104, -79.407785],
    ]),
    ("queen-west", [
        [43.641753, -79.391048],
        [43.648938, -79.41227],
    ]),
    ("queen-west", [
        [43.640439, -79.40094],
        [43.643638, -79.410735],
    ]),
    ("liberty-village", [
        [43.637706, -79.411068],
        [43.644818, -79.427682],
    ]),
    ("liberty-village", [
        [43.635904, -79.417849],
        [43.639165, -79.426863],
    ]),
    ("ossington", [
        [43.643739, -79.417977],
        [43.64894, -79.421411],
    ]),
    ("ossington", [
        [43.648905, -79.420209],
        [43.658337, -79.423728],
    ]),
    ("ossington", [
        [43.652631, -79.422354],
        [43.662062, -79.425874],
    ]),
    ("bloor-west", [
        [43.657689, -79.427537],
        [43.667313, -79.452792],
    ]),
    ("bloor-west", [
        [43.661725, -79.407195],
        [43.671348, -79.432451],
    ]),
    ("bloor-west", [
        [43.667251, -79.388999],
        [43.676873, -79.414255],
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
    "dundas": [43.6552859, -79.3797379],
    "st_patrick": [43.6538735, -79.3832671],
    "queens_park": [43.6538735, -79.3832671],
    "museum": [43.663281, -79.3969142],
    "spadina": [43.663281, -79.3969142],
    "st_george": [43.663281, -79.3969142],
    "wellesley": [43.663281, -79.3969142],
    "bloor_yonge": [43.663281, -79.3969142],
    "bay": [43.6634052, -79.3968713],
    'dupont': [43.6670063, -79.4074714],
    'bathurst': [43.6629395, -79.4161832],
    'christie': [43.6629395, -79.4161832],
    'ossington': [43.6603316, -79.4264829],
    'dufferin': [43.6582514, -79.4377267]
}




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
