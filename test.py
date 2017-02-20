from craigslist import CraigslistHousing
import settings
from slackclient import SlackClient

# cl_h = CraigslistHousing(site=settings.CRAIGSLIST_SITE, area="tor", category=settings.CRAIGSLIST_HOUSING_SECTION,
#                          filters={'max_price': settings.MAX_PRICE, "min_price": settings.MIN_PRICE})
#
# results = []
#
# gen = cl_h.get_results(sort_by='newest', geotagged=True, limit = 100)
#
# i=1
# while True:
#     try:
#         result = next(gen)
#         print (i,result)
#         i+=1
#     except:
#         i+=1
#         pass
#
# extra_filters = {
#     'private_room': {'url_key': 'private_room', 'value': 1},
#     'private_bath': {'url_key': 'private_bath', 'value': 1},
#     'cats_ok': {'url_key': 'pets_cat', 'value': 1},
#     'dogs_ok': {'url_key': 'pets_dog', 'value': 1},
#     'min_price': {'url_key': 'min_price', 'value': None},
#     'max_price': {'url_key': 'max_price', 'value': None},
#     'min_ft2': {'url_key': 'minSqft', 'value': None},
#     'max_ft2': {'url_key': 'maxSqft', 'value': None},
#     'search_distance': {'url_key': 'search_distance', 'value': None},
#     'zip_code': {'url_key': 'postal', 'value': None},
#     'bedrooms': {'url_key': 'bedrooms', 'value': None},
#     'bathrooms': {'url_key': 'bathrooms', 'value': None},
#     'no_smoking': {'url_key': 'no_smoking', 'value': 1},
#     'is_furnished': {'url_key': 'is_furnished', 'value': 1},
#     'wheelchair_acccess': {'url_key': 'wheelchaccess', 'value': 1},
# }


## https://toronto.craigslist.ca/search/apa?s=0&availabilityMode=0&hasPic=1&max_price=1800&min_price=1000&postal=M5J1E6&search_distance=5

url = 'https://images.craigslist.org/00V0V_fFko0HdPRs_600x450.jpg'

sc = SlackClient(settings.SLACK_TOKEN)

channel = 'craigslist'
desc = "distillery | $1775 | 1.5317701447637444 | King/Parliament 1Bdrm. Condo, Avail Immediately! | http://toronto.craigslist.org/tor/apa/6009861700.html"

#
# attachments = [
#         {
#             "fallback": "Required plain-text summary of the attachment.",
#             "author_link": "http://flickr.com/bobby/",
#             "author_icon": "http://flickr.com/icons/bobby.jpg",
#             'author': 'bobby tables',
#             "title": "King/Parliament 1Bdrm. Condo, Avail Immediately!",
#             "text" : "none",
#             "title_link": "http://toronto.craigslist.org/tor/apa/6009861700.html",
#             "thumb_url": "https://images.craigslist.org/00V0V_fFko0HdPRs_600x450.jpg"
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
#         },
# 		 {
#             "fallback": "Required plain-text summary of the attachment.",
#             "footer": "apartment-finder-bot",
#             "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png"
#         }
#     ]

attachments = [
        {
            "fallback": "Required plain-text summary of the attachment.",
            "title": "King/Parliament 1Bdrm. Condo, Avail Immediately!",
            "title_link": "http://toronto.craigslist.org/tor/apa/6009861700.html",
            "thumb_url": "http://i.ebayimg.com/00/s/MzYwWDI3MA==/z/ICkAAOSw2xRYmMMi/$_35.JPG"
        },
		 {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "good",
            "text": "Price: 1650"
        },
         {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "danger",
            "text": "neighborhood: HARLEM"
        },
        {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "warning",
            "text": "Distance to transit: 1.52km"
        }
    ]
# text = desc
sc.api_call(
    "chat.postMessage", channel=channel, attachments = attachments,
    username='apartment-finder-bot', icon_emoji=':robot_face:'
    )
#
#
# sc.api_call(
#     "chat.postMessage", channel=channel, text = 'claire + me',
#     username='sarr', icon_emoji=':burrito:', as_user=False
#     )
