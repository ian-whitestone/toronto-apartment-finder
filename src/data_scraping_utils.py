import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
from lxml import html
import settings
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

def get_html(url):
    r = Render(url)
    html = r.frame.toHtml()
    return html


api_key = settings.GOOGLE_TOKEN

def get_coords(address):
    req_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'
    address = address + ' Toronto, Ontario, Canada'

    try:
        response = requests.get(req_url.format(address,api_key))
        response_dict = response.json()
        coords=response_dict['results'][0]['geometry']['location']
        if response_dict['status'] == 'OK':
            return coords['lat'],coords['lng']
    except Exception as err:
        print ('error retrieving address %s. Error %s' % (address, str(err)))
    return None, None
