## standard library imports
import time

## third party library imports
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Browser():
    def __init__(self,):
        self.driver = webdriver.Chrome()

    def scrape_url(self, url):
        self.driver.get(url)
        time.sleep(10)
        html = self.driver.page_source
        return html
