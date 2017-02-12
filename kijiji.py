
##scraping modules
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import urllib.error

##other modules
import math
import re

## constants

distance = 2.0 # km from postal code
min_price = 0
max_price = 1800

unit_type = {
    'studio': 'b-bachelor-studio',
    '1bed': 'b-1-bedroom',
    '1bed_den': 'b-1-bedroom-den',
    'all': 'b-apartments-condos',
    'house': 'b-house-rental'
    }

def get_soup(url):
    # print (url)
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    shtml = response.read()
    soup = BeautifulSoup(shtml,"html.parser")
    return soup

def parse_address(ad_table):
    for tr in ad_table.findAll('tr'):
        try:
            th = tr.find('th').get_text()
            if th == 'Address':
                address = tr.find('td').get_text().split('\n')[0]
                return address
        except:
            pass
        address = None

    return address

def parse_listings(soup):
    ad_dicts = []
    listings = soup.findAll('div',{'data-ad-id':re.compile('\d{10}')})

    for listing in listings:
        # print (listing['data-ad-id'], listing['data-vip-url'])
        ad_id = listing['data-ad-id']
        listing_url = "http://www.kijiji.ca" + listing['data-vip-url'].split('?src=')[0]
        title = listing_url.split('/')[-2]
        listing_soup = get_soup(listing_url)

        ad_table = listing_soup.find('table', {'class': 'ad-attributes'})
        address = parse_address(ad_table)

        desc = listing_soup.find('span', {'itemprop': 'description'}).get_text()
        desc = desc.strip().replace('\r','').replace('\t','')
        price = listing_soup.find('span', {'itemprop': 'price'}).get_text()

        ad_dict = {
            'title': title,
            'desc': desc,
            'price': price,
            'url': listing_url,
            'id': ad_id,
            'address': address
        }

        ad_dicts.append(ad_dict)
    return ad_dicts

def find_listings():
    listings_dicts = []

    for unit in ['all','house']:
        main_url = 'http://www.kijiji.ca/' + unit_type[unit] + \
            '-apartments-condos/city-of-toronto/c212l1700273r' + str(distance) + \
            '?ad=offering&price=' + str(min_price) + '__' + str(max_price) + \
            '&minNumberOfImages=1&address=M5J+1E6&ll=43.645101,-79.381576&furnished=0'

        soup = get_soup(main_url)
        ads = parse_listings(soup)
        listings_dicts += ads
        next_page = soup.find('a', {'title': 'Next'})

        while next_page:
            soup = get_soup('http://www.kijiji.ca' + next_page['href'])
            ads = parse_listings(soup)
            listings_dicts += ads
            next_page = soup.find('a', {'title':'Next'})

    return listings_dicts



## TO DO
# scrape street address, postal, phone number, availability from ad
# convert address to lat/lon from goodle maps api


# ## not required anymore since you just check for "Next" button
# showing = soup.find("div", {"class": "showing"})
# num_listings = showing.get_text().strip().split()[-2]
# num_pages = math.ceil(int(num_listings)/20)
