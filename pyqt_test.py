import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
from lxml import html
from slackclient import SlackClient
from bs4 import BeautifulSoup
import requests

#https://impythonist.wordpress.com/2015/01/06/ultimate-guide-for-scraping-javascript-rendered-web-pages/

#Take this class for granted.Just use result of rendering.
class Render(QWebPage):
  def __init__(self, url):
    self.app = QApplication(sys.argv)
    QWebPage.__init__(self)
    self.loadFinished.connect(self._loadFinished)
    self.mainFrame().load(QUrl(url))
    self.app.exec_()

  def _loadFinished(self, result):
    self.frame = self.mainFrame()
    self.app.quit()

url = "https://toronto.craigslist.ca/search/apa?s=0&availabilityMode=0&hasPic=1&max_price=1800&min_price=1000&postal=M5J1E6&search_distance=5"
r = Render(url)
result = r.frame.toHtml()

soup = BeautifulSoup(result, 'html.parser')

rows = soup.find_all('p', {'class': 'result-info'})
listings = soup.find_all('li', {'class': 'result-row'})

for row,listing in zip(rows,listings):
    link = row.find('a', {'class': 'hdrlnk'})
    id = link.attrs['data-id']
    name = link.text

    print (id)
    print (listing.find('img'))
