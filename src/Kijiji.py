## standard library imports
import urllib.request
import urllib.parse
import urllib.error
import logging as log
import math
import re

## third party library imports
from bs4 import BeautifulSoup

## local library imports
import src.settings as settings
import src.Google as Google


class Kijiji():
    """ """

    def __init__(self):
        coords = Google.get_coords(settings.POSTAL)
        self.postal_lat = str(round(coords[0],5))
        self.postal_lon = str(round(coords[1],5))
        if len(self.postal_lat.split('.')[1])<5:
            self.postal_lat += '0'
        if len(self.postal_lon.split('.')[1])<5:
            self.postal_lon += '0'

    def get_soup(self, url):
        # print (url)
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        shtml = response.read()
        soup = BeautifulSoup(shtml, "html.parser")
        return soup

    def parse_address(self, ad_table):
        for tr in ad_table.findAll('tr'):
            try:
                th = tr.find('th').get_text()
                if th == 'Address':
                    address = tr.find('td').get_text().split('\n')[0]
                    address = address.split(',')[0]
                    return address
            except:
                pass
            address = None

        return address

    def parse_listings(self, soup):
        ad_dicts = []
        listings = soup.findAll('div',{'data-ad-id':re.compile('\d{10}')})

        for listing in listings:
            # print (listing['data-ad-id'], listing['data-vip-url'])
            ad_id = listing['data-ad-id']
            listing_url = "http://www.kijiji.ca" + listing['data-vip-url'].split('?src=')[0]
            title = listing_url.split('/')[-2]
            listing_soup = self.get_soup(listing_url)

            ad_table = listing_soup.find('table', {'class': 'ad-attributes'})
            address = self.parse_address(ad_table)

            desc = listing_soup.find('span', {'itemprop': 'description'}).get_text()
            desc = desc.strip().replace('\r','').replace('\t','')
            price = listing_soup.find('span', {'itemprop': 'price'}).get_text()

            image = None
            try:
                image_parent = listing_soup.find('li', {'class': 'showing'})
                if image_parent:
                    image = image_parent.find('img', {'itemprop': 'image'})['src']
            except Exception as e:
                # print ('error finding kijiji image. Error %s' % str(e))
                pass

            ad_dict = {
                'title': title,
                'desc': desc,
                'price': price,
                'url': listing_url,
                'id': ad_id,
                'address': address,
                'image_url': image
            }

            ad_dicts.append(ad_dict)
        return ad_dicts

    def build_url(self, unit):
        base_url = 'http://www.kijiji.ca/' + settings.UNIT_TYPE_MAP[unit]


        url = (base_url + 'r' + str(settings.SEARCH_DISTANCE) + '?ad=offering&price='
            + str(settings.MIN_PRICE) + '__' + str(settings.MAX_PRICE)
            + '&minNumberOfImages=' + str(settings.HAS_IMAGE)
            + '&address=' + settings.POSTAL +'&ll=' + str(self.postal_lat)
            + ',' + str(self.postal_lon)
            + '&furnished=' + str(settings.FURNISHED)
            )

        return url

    def find_listings(self):
        listings_dicts = []

        for unit in settings.UNIT_TYPES:
            main_url = self.build_url(unit)
            soup = self.get_soup(main_url)
            ads = self.parse_listings(soup)
            listings_dicts += ads
            next_page = soup.find('a', {'title': 'Next'})

            i = 1
            if settings.TESTING:
                max_pages = 1
            else:
                max_pages = 10

            while next_page and i < max_pages: ## only do 10 pages (1 already done above)
                i += 1
                soup = self.get_soup('http://www.kijiji.ca' + next_page['href'])
                ads = self.parse_listings(soup)
                listings_dicts += ads
                next_page = soup.find('a', {'title':'Next'})

        return listings_dicts
