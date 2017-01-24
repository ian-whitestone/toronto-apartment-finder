from craigslist import CraigslistHousing
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse
from util import post_listing_to_slack, find_points_of_interest, post_favourite, match_neighbourhood
from slackclient import SlackClient
import time
import settings
import slacker
import re

engine = create_engine('sqlite:///listings.db', echo=False)

Base = declarative_base()

class Listing(Base):
    """
    A table to store data on craigslist listings.
    """

    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    created = Column(DateTime)
    geotag = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    name = Column(String)
    price = Column(Float)
    location = Column(String)
    cl_id = Column(Integer, unique=True)
    area = Column(String)
    metro_stop = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def scrape_area(area):
    """
    Scrapes craigslist for a certain geographic area, and finds the latest listings.
    :param area:
    :return: A list of results.
    """

    cl_h = CraigslistHousing(site=settings.CRAIGSLIST_SITE, area=area, category=settings.CRAIGSLIST_HOUSING_SECTION,
                             filters={'max_price': settings.MAX_PRICE, "min_price": settings.MIN_PRICE})

    results = []

    gen = cl_h.get_results(sort_by='newest', geotagged=True, limit=50)
    neighborhoods = []
    while True:
        try:
            result = next(gen)
            neighborhoods.append(result['where'])
        except StopIteration:
            break
        except Exception:
            continue
        listing = session.query(Listing).filter_by(cl_id=result["id"]).first()

        # Don't store the listing if it already exists.
        if listing is None:
            if result["where"] is None and result["geotag"] is not None:
                # If there is no string identifying which neighborhood the result is from or no geotag, skip it.
                continue

            lat = 0
            lon = 0
            if result["geotag"] is not None:
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
            listing = Listing(
                link=result["url"],
                created=parse(result["datetime"]),
                lat=lat,
                lon=lon,
                name=result["name"],
                price=price,
                location=result["where"],
                cl_id=result["id"],
                area=result["area"],
                metro_stop=result["metro"]
            )

            # Save the listing so we don't grab it again.
            session.add(listing)
            session.commit()

            # Return the result if it has images, it's near a metro station, or if it is in an area we defined.
            if result['has_image'] and (len(result["metro"]) > 0 or len(result["area"]) > 0) and check_title(result['name']):
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

def get_posted_favourites(bot,channel_dict):
    channel_id = channel_dict['favourites']
    response = bot.channels.history(channel_id)

    posted_ids = []
    for message in response.body['messages']:
        try:
            posted_ids.append(message['text'].split('.html')[0].split('apa/')[1])
        except:
            pass

    return posted_ids

def post_favourites():
    bot = slacker.Slacker(settings.SLACK_TOKEN)
    channels_response = bot.channels.list()
    channel_dict = {chan['name']:chan['id'] for chan in channels_response.body['channels']}

    posted_ids = get_posted_favourites(bot,channel_dict)

    channel_id = channel_dict['housing']
    response = bot.channels.history(channel_id)

    for message in response.body['messages']:
        try:
            cl_id = message['text'].split('.html')[0].split('apa/')[1]
        except:
            continue

        reactions = message.get('reactions',None)
        if reactions:
            for reaction in reactions:
                if reaction['name'] == '+1' and reaction['count'] > 1 and cl_id not in posted_ids:
                    post_favourite(bot,message['text'])
                    continue
    return

def do_scrape():
    """
    Runs the craigslist scraper, and posts data to slack.
    """

    # Create a slack client.
    sc = SlackClient(settings.SLACK_TOKEN)

    # Get all the results from craigslist.
    all_results = []
    for area in settings.AREAS:
        all_results += scrape_area(area)

    print("{}: Got {} results".format(time.ctime(), len(all_results)))

    # Post each result to slack.
    for result in all_results:
        post_listing_to_slack(sc, result)
