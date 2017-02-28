## standard library imports
import logging as log

## third party library imports
import slacker
from slackclient import SlackClient

## local library imports
import src.settings as settings

session = create_sqlite_session()

def get_posted_favourites():
    favourites = session.query(Favourites).all()
    links = [fav.link for fav in favourites]
    return links


def post_favourites():
    bot = slacker.Slacker(settings.SLACK_TOKEN)
    channels_response = bot.channels.list()
    channel_dict = {chan['name']:chan['id']
        for chan in channels_response.body['channels']}
    posted_favourites = get_posted_favourites()

    channels = list(set([c for key,c in settings.SLACK_CHANNELS.items()]))

    # Create a slack client.
    sc = SlackClient(settings.SLACK_TOKEN)

    for channel in channels:
        channel_id = channel_dict[channel]
        response = bot.channels.history(channel_id)

        for message in response.body['messages']:
            if 'attachments' not in message.keys():
                continue

            attachment = message['attachments'][0]
            title = attachment['title']
            link = attachment['title_link']
            desc = attachment['fallback']

            reactions = message.get('reactions', None)
            if reactions:
                for reaction in reactions:
                    if reaction['name'] == '+1' and reaction['count'] > 1 \
                        and link not in posted_favourites:
                        post_and_hist_favourite(sc, title, link, desc)
                        break
    return

def post_and_hist_favourite(sc, title, link, desc):
    post = [
        {
            "fallback": 'N/A',
            'color': settings.DEFAULT_COLOUR,
            "text": desc
        }
    ]

    post_favourite(sc, post)
    listing = Favourites(link=link, title=title)
    session.add(listing)
    session.commit()
    return

def post_favourite(sc, attachment):
    sc.api_call(
        "chat.postMessage", channel='favourites', attachments=attachment,
        username=settings.SLACK_BOT, icon_emoji=':robot_face:'
    )

    return
