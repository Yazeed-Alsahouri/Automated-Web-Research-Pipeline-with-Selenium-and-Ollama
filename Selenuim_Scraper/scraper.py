from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time
import random
from selenium.webdriver.common.keys import Keys
from .scrape_pages import PageScraper
from sipbuild.generator.utils import search_typedefs

from . import consts
import os
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class WebScraper(webdriver.Chrome):

    def __init__(self ,driver_path = "C:/SeleniumDrivers" ,auto_close = False):

        self.driver_path = driver_path
        self.auto_close = auto_close

        os.environ["PATH"] += self.driver_path
        super(WebScraper, self).__init__()

        self.implicitly_wait(30)
        self.maximize_window()

    def __exit__(self ,exc_type ,exc_val ,exc_tb):
        if self.auto_close:
            self.quit()

    def user_search(self ,text):
        page_url = consts.PAGE_URL

        try:
            self.get(page_url)
            search_box = WebDriverWait(self ,15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR ,'input[id="searchbox_input"]'))
            )
            search_box.send_keys(text ,Keys.ENTER)

        except Exception as e:
            print(f"There is an error in getting the page : {e}")


    def scrape_data(self):

        scraper = PageScraper(driver=self)

        return scraper.scrape_main_page()

























