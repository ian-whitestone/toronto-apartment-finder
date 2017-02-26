## standard library imports
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
from lxml import html
import requests
import time

## third party library imports
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

## local library imports
import src.settings as settings

#https://impythonist.wordpress.com/2015/01/06/ultimate-guide-for-scraping-javascript-rendered-web-pages/

# DEPRECATED....TOO UNSTABLE
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
    r.app.quit()
    r.frame = None
    r.mainFrame = None
    return html

class Browser():
    def __init__(self,):
        self.driver = webdriver.Chrome()

    def scrape_url(self, url):
        self.driver.get(url)
        time.sleep(10)
        html = self.driver.page_source
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

## http://stackoverflow.com/questions/21909907/pyqt-class-not-working-for-the-second-usage/21918243#21918243
