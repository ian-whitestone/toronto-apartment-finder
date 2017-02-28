## standard library imports
import math
import logging as log

## third party library imports
import slacker

## local library imports
import src.settings as settings


def coord_distance(lat1, lon1, lat2, lon2):
    """
    Finds the distance between two pairs of latitude and longitude.
    :param lat1: Point 1 latitude.
    :param lon1: Point 1 longitude.
    :param lat2: Point two latitude.
    :param lon2: Point two longitude.
    :return: Kilometer distance.
    """
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return round(km,2)

def in_box(coords, box):
    """
    Find if a coordinate tuple is inside a bounding box.
    :param coords: Tuple containing latitude and longitude.
    :param box: Two tuples, where first is the bottom left, and the second is the top right of the box.
    :return: Boolean indicating if the coordinates are in the box.
    """
    if box[0][0] < coords[0] < box[1][0] and box[1][1] < coords[1] < box[0][1]:
        return True
    return False

def post_listing_to_slack(sc, listing, site):
    """
    Posts the listing to slack.
    :param sc: A slack client.
    :param listing: A record of the listing.
    :param site: craigslist or kijiji
    """
    if settings.TESTING:
        channel = settings.TESTING_CHANNEL
    else:
        channel = settings.SLACK_CHANNELS.get(listing['area'],
            settings.DEFAULT_CHANNEL)

    if settings.ENHANCED_POSTS:
        attachment = build_attachment(listing, site)
    else:
        attachment = {"fallback": desc, 'color': settings.DEFAULT_COLOUR,
            'text': desc}

    sc.api_call(
        "chat.postMessage", channel=channel, attachments=attachment,
        username=settings.SLACK_BOT, icon_emoji=':robot_face:'
    )
    return

def get_desc(listing, site):
    if site == 'craigslist':
        desc = "{0} | {1} | {2} | {3} | <{4}>".format(listing["area"],
            listing["price"], listing["metro_dist"],
            listing["title"], listing["url"])
    elif site == 'kijiji':
        desc = "{0} | {1} | <{2}>".format(listing['price'],
            listing['title'], listing["url"])
    else:
        desc = "No description"
    return desc

def build_attachment(listing, site):
    attachments = []

    desc = get_desc(listing, site)

    header = {
        "fallback": desc,
        'color': settings.DEFAULT_COLOUR,
        "title": listing.get('title',None),
        "title_link": listing.get('url',None),
        "image_url": listing.get('image_url',None)
        # "thumb_url": listing.get('image_url',None)
    }

    attachments.append(header)

    fields = get_attachment_fields(listing, site)
    attachments += fields

    return attachments



def get_attachment_fields(listing, site):
    attachments = []
    post_fields = settings.SLACK_PARAMS[site]

    colours = {key:get_colour(key, listing)
        for key, field_desc in post_fields.items()}

    fields = [{'short': True, 'value': field_desc + str(listing.get(key,''))}
        for key, field_desc in post_fields.items()
        if colours[key] == settings.DEFAULT_COLOUR
        ]

    if fields:
        payload = {
            'fallback': 'N/A',
            'color': settings.DEFAULT_COLOUR,
            'fields': fields
            }
        attachments.append(payload)

    for param in settings.COLOUR_PARAM_ORDER:
        payload = {
            'fallback': 'N/A',
            'color': colours[param],
            'text': post_fields[param] + str(listing.get(param,''))
        }
        attachments.append(payload)

    return attachments

def OLD_get_attachment_fields(listing, site):
    attachments = []
    post_fields = settings.SLACK_PARAMS[site]

    colours = {key:get_colour(key, listing)
        for key, field_desc in post_fields.items()}

    for colour in settings.COLOUR_ORDER:
        fields = [{'short': True, 'value': field_desc + str(listing.get(key,''))}
            for key, field_desc in post_fields.items() if colours[key] == colour]

        if fields:
            payload = {
                'fallback': 'N/A',
                'color': colour,
                'fields': fields
            }
            attachments.append(payload)

    return attachments

def get_colour(key, listing):
    """Score feature with a colour based on preferred ranges
    params
        key: feature
        listing: listing dict from scraper module
    return
        colour: good (green), warning(yellow), danger (red)
    """
    colours = settings.COLOURS
    try:
        if key in colours.keys() and key in listing.keys():
            colour_dict = colours[key]

            if colour_dict['type'] == 'range':
                if isinstance(listing[key], str):
                    value = float(listing[key].replace('$','').replace(',',''))
                else:
                    value = float(listing[key])

                for colour, scale in colour_dict['levels'].items():
                    if value >= scale[0] and value <= scale[1]:
                        return colour
            else:
                value = listing[key]
                for colour, levels in colour_dict['levels'].items():
                    if value in levels:
                        return colour

            return settings.DEFAULT_COLOUR
    except:
        return settings.DEFAULT_COLOUR

    return settings.DEFAULT_COLOUR

def find_points_of_interest(geotag):
    """
    Find points of interest, like transit, near a result.
    :param geotag: The geotag field of a Craigslist result.
    :return: A dictionary containing annotations.
    """
    area_found = False
    area = ""
    min_dist = None
    near_metro = False
    metro_dist = "N/A"
    metro = ""
    # Look to see if the listing is in any of the neighborhood boxes we defined.
    for hood in settings.BOXES:
        name = hood[0]
        coords = hood[1]
        if in_box(geotag, coords):
            area = name
            area_found = True
            break

    # Check to see if the listing is near any transit stations.
    for station, coords in settings.TRANSIT_STATIONS.items():
        dist = coord_distance(coords[0], coords[1], geotag[0], geotag[1])

        if (min_dist is None or dist < min_dist) and dist < settings.MAX_TRANSIT_DIST:
            near_metro = True

        if (min_dist is None or dist < min_dist):
            metro_dist = dist
            min_dist = dist
            metro = station

    return {
        "area_found": area_found,
        "area": area,
        "near_metro": near_metro,
        "metro_dist": metro_dist,
        "metro": metro
    }

def match_neighbourhood(location):
    """
    Find points of interest, like transit, near a result.
    :param location: The where field of a Craigslist result.  Is a string containing a description of where
    the listing was posted.
    :return: A dictionary containing annotations.
    """
    area_found = False
    area = ""
    min_dist = None
    near_metro = False
    metro_dist = "N/A"
    metro = ""

    # If the listing isn't in any of the boxes we defined, check to see if the string description of the neighborhood
    # matches anything in our list of neighborhoods.
    for hood in settings.NEIGHBORHOODS:
        if hood.lower() in location.lower():
            area = hood

    return {
        "area_found": area_found,
        "area": area,
        "near_metro": near_metro,
        "metro_dist": metro_dist,
        "metro": metro
    }
