## standard library imports
import time
import re
from dateutil.parser import parse
import logging as log

## third party library imports
import slacker
from slackclient import SlackClient

## local library imports
from src.Craigslist import CraigslistHousing
import src.Kijiji as kijiji
from src.GeneralUtils import post_listing_to_slack, find_points_of_interest, match_neighbourhood
import src.settings as settings
from src.DatabaseOperations import ClListing, KjListing, create_sqlite_session
from src.Google import get_coords



session = create_sqlite_session()
def getCraigslistGen(area):
    log.info('getting Craigslist generator')
    cl_h = CraigslistHousing(
        site=settings.CRAIGSLIST_SITE, area=area,
        category=settings.CRAIGSLIST_HOUSING_SECTION,
        filters={
            'max_price': settings.MAX_PRICE,
            "min_price": settings.MIN_PRICE,
            "hasPic": settings.HAS_IMAGE,
            "postal": settings.POSTAL,
            "search_distance": settings.SEARCH_DISTANCE
            }
        )

    gen = cl_h.get_results(sort_by='newest', geotagged=True, limit = 100)
    return gen

def checkResult(result):
    listing = session.query(ClListing).filter_by(id=result["id"]).first()
    result_check = True
    # Don't store the listing if it already exists.
    if listing is not None and settings.TESTING == False:
        result_check = False

    if result["where"] is None and result["geotag"] is None:
        # If there is no string identifying which neighborhood the result is from or no geotag, skip it.
        result_check = False

    return result_check
def getGeoInfo(result):
    if result["geotag"]:
        # Assign the coordinates.
        result['lat'] = result["geotag"][0]
        result['lon'] = result["geotag"][1]

        # Annotate the result with information about the area it's in and points of interest near it.
        geo_data = find_points_of_interest(result["geotag"])
        result.update(geo_data)
    else:
        result['lat'] = 0
        result['lon'] = 0
        geo_data = match_neighbourhood(result['where'])
        result.update(geo_data)
    return result

def scrapeCraigslist(area):
    """
    Scrapes craigslist for a certain geographic area, and finds the latest listings.
    :param area:
    :return: A list of results.
    """

    gen = getCraigslistGen(area)
    results = []
    while True:
        try:
            result = next(gen)
        except StopIteration:
            break
        except Exception as err:
            log.exception('An exception occured %s' % str(err))
            continue

        if checkResult(result) == False:
            continue

        result = getGeoInfo(result)

        # Try parsing the price.
        try:
            result['price'] = float(result["price"].replace("$", ""))
        except Exception as err:
            log.exception('Error parsing price for result: %s Error: %s'
                % (result,str(err)))

        histCLListing(result)

        # Return the result if it has images and it is in an area we defined.
        # can modify the second condition so it check if it's in the area
        # OR within MAX_TRANSIT_DIST
        if result['has_image'] and len(result["area"]) > 0 \
            and checkTitle(result['title']):
            results.append(result)

    return results

def histCLListing(result):
    # Create the listing object.
    listing = ClListing(
        link=result["url"],
        created=parse(result["datetime"]),
        lat=result['lat'],
        lon=result['lon'],
        title=result["title"],
        price=result.get('price',0),
        location=result["where"],
        id=result["id"],
        area=result["area"],
        metro_stop=result["metro"]
    )

    # Save the listing so we don't grab it again.
    if not settings.TESTING:
        session.add(listing)
        session.commit()
    return

def checkTitle(name):
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


def scrapeKijiji():
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
                if len(result["area"]) == 0 or checkTitle(result['title']) == False:
                    ## len(result["metro"]) == 0 or ## old subway dist filter
                    ## if it's not within X km of subway or in specified area, pass
                    continue

            results.append(result)
        except:
            log.exception('errored on ' % result)
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
            log.info('scraping Craigslist area %s' % area)
            all_results += scrapeCraigslist(area)
            pass

        log.info("{}: Got {} results for Craigslist".format(time.ctime(), len(all_results)))

        # Post each result to slack.
        for result in all_results:
            post_listing_to_slack(sc, result, 'craigslist')

    if settings.KIJIJI:
        # Get all the results from kijiji.
        log.info('scraping kijiji')
        all_results = scrapeKijiji()

        log.info("{}: Got {} results from Kijiji".format(time.ctime(), len(all_results)))

        for result in all_results:
            post_listing_to_slack(sc, result, 'kijiji')

    return
