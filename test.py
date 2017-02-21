from src.craigslist import CraigslistHousing
import src.settings as settings
from slackclient import SlackClient
from bs4 import BeautifulSoup
import requests
import src.util as util

# sc = SlackClient(settings.SLACK_TOKEN)
#
# listing = {'title' : 'test', 'price': '$1500', 'url': 'http://toronto.craigslist.org/tor/apa/6011116782.html',
# 'image_url': 'https://images.craigslist.org/00l0l_3Sr1PSsH4fd_300x300.jpg'}
#
# util.post_listing_to_slack(sc, listing, 'kijiji')

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
#
for i in range(1,101):
    result = next(gen)
    print (i,result)


# url = "https://toronto.craigslist.ca/search/apa?s=0&availabilityMode=0&hasPic=1&max_price=1800&min_price=1000&postal=M5J1E6&search_distance=5"
#
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')
#
# rows = soup.find_all('p', {'class': 'result-info'})
# listings = soup.find_all('li', {'class': 'result-row'})
#
# for row,listing in zip(rows,listings):
#     link = row.find('a', {'class': 'hdrlnk'})
#     id = link.attrs['data-id']
#     name = link.text
#
#     print (id)
#     print (listing)
#     break

# url = 'https://images.craigslist.org/00V0V_fFko0HdPRs_600x450.jpg'
#
# sc = SlackClient(settings.SLACK_TOKEN)
#
# channel = 'craigslist'
# desc = "distillery | $1775 | 1.5317701447637444 | King/Parliament 1Bdrm. Condo, Avail Immediately! | http://toronto.craigslist.org/tor/apa/6009861700.html"
#
# # 		 {
# #             "fallback": "Required plain-text summary of the attachment.",
# #             "footer": "apartment-finder-bot",
# #             "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png"
# #         }
#
#
# attachments = [
#         {
#             "fallback": "Required plain-text summary of the attachment.",
#             "title": "King/Parliament 1Bdrm. Condo, Avail Immediately!",
#             "title_link": "http://toronto.craigslist.org/tor/apa/6009861700.html",
#             "thumb_url": "http://i.ebayimg.com/00/s/MzYwWDI3MA==/z/ICkAAOSw2xRYmMMi/$_35.JPG"
#         },
# 		 {
#             "fallback": "Required plain-text summary of the attachment.",
#             "color": "good",
#             "text": "Price: 1650"
#         },
#          {
#             "fallback": "Required plain-text summary of the attachment.",
#             "color": "danger",
#             "text": "neighborhood: HARLEM"
#         },
#         {
#             "fallback": "Required plain-text summary of the attachment.",
#             "color": "warning",
#             "text": "Distance to transit: 1.52km"
#         }
#     ]
#
# sc.api_call(
#     "chat.postMessage", channel=channel, attachments = attachments,
#     username='apartment-finder-bot', icon_emoji=':robot_face:'
#     )
