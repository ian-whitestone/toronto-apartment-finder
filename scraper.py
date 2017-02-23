from src.craigslist import CraigslistHousing
import src.kijiji as kijiji
from src.util import post_listing_to_slack, find_points_of_interest, post_favourite, match_neighbourhood
import src.settings as settings
from database_operations import ClListing, KjListing, create_sqlite_session
from src.data_scraping_utils import get_coords

from dateutil.parser import parse
from slackclient import SlackClient
import time
import slacker
import re

session = create_sqlite_session()

def scrape_area(area):
    """
    Scrapes craigslist for a certain geographic area, and finds the latest listings.
    :param area:
    :return: A list of results.
    """

    cl_h = CraigslistHousing(
        site=settings.CRAIGSLIST_SITE, area="tor",
        category=settings.CRAIGSLIST_HOUSING_SECTION,
        filters={
            'max_price': settings.MAX_PRICE,
            "min_price": settings.MIN_PRICE,
            "hasPic": settings.HAS_IMAGE,
            "postal": settings.POSTAL,
            "search_distance": settings.SEARCH_DISTANCE
            }
        )

    results = []

    gen = cl_h.get_results(sort_by='newest', geotagged=True, limit = 100)
    neighborhoods = []
    while True:
        try:
            result = next(gen)
            neighborhoods.append(result['where'])
        except StopIteration:
            break
        except Exception:
            continue

        listing = session.query(ClListing).filter_by(id=result["id"]).first()

        # Don't store the listing if it already exists.
        if listing is None and not settings.TESTING:
            if result["where"] is None and result["geotag"] is None:
                # If there is no string identifying which neighborhood the result is from or no geotag, skip it.
                continue

            lat = 0
            lon = 0
            if result["geotag"]:
                # Assign the coordinates.
                lat = result["geotag"][0]
                lon = result["geotag"][1]

                # Annotate the result with information about the area it's in and points of interest near it.
                geo_data = find_points_of_interest(result["geotag"])
                result.update(geo_data)
            else:
                geo_data = match_neighbourhood(result['where'])
                result.update(geo_data)

            # Try parsing the price.
            price = 0
            try:
                price = float(result["price"].replace("$", ""))
            except Exception:
                pass

            # Create the listing object.
            listing = ClListing(
                link=result["url"],
                created=parse(result["datetime"]),
                lat=lat,
                lon=lon,
                title=result["title"],
                price=price,
                location=result["where"],
                id=result["id"],
                area=result["area"],
                metro_stop=result["metro"]
            )

            # Save the listing so we don't grab it again.
            if not settings.TESTING:
                session.add(listing)
                session.commit()

            # Return the result if it has images, it's near a metro station,
            # or if it is in an area we defined.
            if result['has_image'] and (len(result["metro"]) > 0  \
                or len(result["area"]) > 0) and check_title(result['title']):
                results.append(result)

    return results

def check_title(name):
    """
    check the listing title to see if it's a studio or furnished
    """
    STUDIO = re.compile('studio',re.IGNORECASE)
    BACHELOR = re.compile('bachelor',re.IGNORECASE)
    FURNISHED = re.compile('furnished',re.IGNORECASE)

    m1 = re.search(STUDIO,name)
    m2 = re.search(FURNISHED,name)
    m3 = re.search(BACHELOR,name)

    if m1 or m2:
        return False
    else:
        return True


def scrape_kijiji():
    base_results = kijiji.find_listings()

    results = []
    for result in base_results:
        try:
            listing = session.query(KjListing).filter_by(id=result["id"]).first()

            ## if listing is already in the db and in production mode, don't append
            if listing and not settings.TESTING:
                continue

            # Create the listing object.
            listing = KjListing(
                id = result['id'],
                link = result['url'],
                price = result['price'],
                title = result['title'],
                address = result['address']
            )

            # Save the listing so we don't grab it again.
            if not settings.TESTING:
                session.add(listing)
                session.commit()

            lat, lon = get_coords(result['address'])
            if lat and lon:
                # Annotate the result with information about the area it's in and points of interest near it.
                geo_data = find_points_of_interest([lat,lon])
                result.update(geo_data)

                ## only scrub listings that we actually verified were out of range
                if len(result["metro"]) == 0 or len(result["area"]) == 0:
                    ## if it's not within X km of subway or in specified area, pass
                    continue

            results.append(result)
        except:
            print ('errored on ' % result)
    return results


def do_scrape():
    """
    Runs the craigslist scraper, and posts data to slack.
    """

    # Create a slack client.
    sc = SlackClient(settings.SLACK_TOKEN)

    # Get all the results from craigslist.
    if settings.CRAIGSLIST:
        all_results = []
        for area in settings.AREAS:
            all_results += scrape_area(area)
            pass

        print("{}: Got {} results for Craigslist".format(time.ctime(), len(all_results)))

        # Post each result to slack.
        for result in all_results:
            post_listing_to_slack(sc, result, 'craigslist')

    if settings.KIJIJI:
        # Get all the results from kijiji.
        all_results = scrape_kijiji()

        print("{}: Got {} results from Kijiji".format(time.ctime(), len(all_results)))

        for result in all_results:
            post_listing_to_slack(sc, result, 'kijiji')

    return


def get_posted_favourites(bot,channel_dict):
    channel_id = channel_dict['favourites']
    response = bot.channels.history(channel_id)

    posted_ids = []
    for message in response.body['messages']:
        try:
            if '.html' in message['text']:
                posted_ids.append(message['text'].split('.html')[0].split('apa/')[1])
            else:
                posted_ids.append(message['text'].split('/')[-1])
        except:
            pass

    return posted_ids


def post_favourites():
    bot = slacker.Slacker(settings.SLACK_TOKEN)
    channels_response = bot.channels.list()
    channel_dict = {chan['name']:chan['id'] for chan in channels_response.body['channels']}
    posted_ids = get_posted_favourites(bot,channel_dict)

    for channel in ['kijiji', 'craigslist']:
        channel_id = channel_dict[channel]
        response = bot.channels.history(channel_id)

        for message in response.body['messages']:
            try:
                if channel == 'craigslist':
                    ad_id = message['text'].split('.html')[0].split('apa/')[1]
                elif channel == 'kijiji':
                    ad_id = message['text'].split('/')[-1]
            except:
                continue

            reactions = message.get('reactions',None)
            if reactions:
                for reaction in reactions:
                    if reaction['name'] == '+1' and reaction['count'] > 1 and ad_id not in posted_ids:
                        post_favourite(bot,message['text'])
                        continue
    return
