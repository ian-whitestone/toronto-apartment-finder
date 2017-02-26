from src.craigslist import CraigslistHousing
import src.settings as settings
from slackclient import SlackClient
from bs4 import BeautifulSoup
import requests
import src.util as util

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
from pprint import pprint

def get_posted_favourites(bot,channel_dict):
    channel_id = channel_dict['testing']
    response = bot.channels.history(channel_id)

    posted_ids = []
    pprint(response.body)

    for message in response.body['messages']:
        attachments = message['attachments']
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
    posted_ids = get_posted_favourites(bot, channel_dict)
    return

post_favourites()
