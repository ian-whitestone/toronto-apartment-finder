
##scraping modules
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import urllib.error

##other modules
import math
import re

def get_soup(url):
    print (url)
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    shtml = response.read()
    soup = BeautifulSoup(shtml,"html.parser")
    return soup


distance = 2.0 # km from postal code
min_price = 0
max_price = 1800

unit_type = {'studio':'b-bachelor-studio','1bed':'b-1-bedroom','1bed_den':'b-1-bedroom-den'}

main_url = 'http://www.kijiji.ca/' + unit_type['1bed'] + '-apartments-condos/city-of-toronto/c212l1700273r' + str(distance) + \
                '?ad=offering&price=' + str(min_price) + '__' + str(max_price) + '&minNumberOfImages=1&address=M5J+1E6&ll=43.645101,-79.381576&furnished=0'

soup = get_soup(main_url)


## not required anymore since you just check for "Next" button
showing = soup.find("div", {"class": "showing"})
num_listings = showing.get_text().strip().split()[-2]
num_pages = math.ceil(int(num_listings)/20)


listings = soup.findAll('div',{'data-ad-id':re.compile('\d{10}')})

# for listing in listings:
    # print (listing['data-ad-id'], listing['data-vip-url'])


next_page = soup.find('a', {'title':'Next'})

while next_page:
    soup = get_soup('http://www.kijiji.ca' + next_page['href'])
    next_page = soup.find('a', {'title':'Next'})

## TO DO
# scrape street address, postal, phone number, availability from ad
