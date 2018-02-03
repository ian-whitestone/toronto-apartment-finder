import time
import logging as log
import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
DRIVER_PATH = os.path.join(CURR_DIR, 'chromedriver')

class Browser():
    def __init__(self,):
        log.info('initializing chrome driver')
        self.driver = webdriver.Chrome(DRIVER_PATH)

    def scrape_url(self, url):
        self.driver.get(url)
        time.sleep(10)
        html = self.driver.page_source
        return html
