import utils
import os

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
KEYS_PATH = os.path.join(CURR_DIR, 'keys.yml')

## Toggle for testing mode
TESTING = True

######################
### SEARCH FILTERS ###
######################

# The minimum rent you want to pay per month.
MIN_PRICE = 0

# The maximum rent you want to pay per month.
MAX_PRICE = 10000

# Kijiji/Craiglist image requirement: 0 or 1
HAS_IMAGE = 1

#Kijiji/postal code to search within
POSTAL = 'M4W1A8'

#distance (km)
SEARCH_DISTANCE = 10

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
    '1bed': 'b-1-bedroom-apartments-condos/city-of-toronto/c212l1700273',
    '2bed': 'b-2-bedroom-apartments-condos/city-of-toronto/c214l1700273',
    '1bed_den': 'b-1-bedroom-den-apartments-condos/city-of-toronto/c213l1700273',
    'all': 'b-apartments-condos/city-of-toronto/c37l1700273',
    'house': 'b-house-rental/city-of-toronto/c43l1700273'
    }

# enter the types of units you would like to parse
# 'all' includes studios, 1beds, 1beds + den
# 'all' DOES NOT INCLUDE houses
UNIT_TYPES = ['all', 'house']

# 0 if you want un-furnished units, 1 for furnished units
FURNISHED = 0

# Directory in your folder where you want the log files stored
LOG_PATH = 'logs'


###############
## LOAD KEYS ##
###############

keys = utils.read_yaml(KEYS_PATH)

GOOGLE_GEOCODE_TOKEN = keys['google']['geocode']
GOOGLE_DIRECTIONS_TOKEN = keys['google']['directions']
