from IPython.utils.frame import extract_vars
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from selenium.webdriver.remote.webdriver import WebDriver
import time
import random
from selenium.webdriver.common.keys import Keys
from sipbuild.generator.utils import search_typedefs

from . import consts
import os
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class PageScraper:

    def __init__(self ,driver:WebDriver):

        self.driver = driver

    def scrape_main_page(self):
        all_text = []

        websites_ol = self.driver.find_element(By.CSS_SELECTOR ,'ol[class="react-results--main"]')

        websites_li = websites_ol.find_elements(By.CSS_SELECTOR ,'li[data-layout="organic"]')


        for web_li in websites_li[1:]:
            all_text.append(self.scrape_website(web_li))

        return all_text

    def scrape_website(self ,web):

        website_link = web.find_element(By.CSS_SELECTOR, 'a[data-testid="result-title-a"]')
        web_href = website_link.get_attribute('href')

        main_tab = self.driver.current_window_handle

        website_text = ""

        try:
            self.driver.switch_to.new_window('tab')
            self.driver.get(web_href)

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            website_text = self.get_text_inside_website(self.driver)

        except Exception as e:
            print(f"There is an error in scraping the websites : {e}")

        finally:
            if len(self.driver.window_handles) > 1:
                self.driver.close()
            self.driver.switch_to.window(main_tab)

        return website_text

    def get_text_inside_website(self, web):

        content_selectors = [
            "article",
            "main",
            "div[id*='content']",
            "div[class*='post-content']",
            "div[class*='article-body']"
        ]

        container = None
        for selector in content_selectors:
            try:

                container = self.driver.find_element(By.CSS_SELECTOR, selector)
                if container.is_displayed():
                    break
            except NoSuchElementException:
                continue


        search_root = container if container else self.driver.find_element(By.TAG_NAME, "body")


        text_elements = search_root.find_elements(
            By.XPATH,
            ".//h1 | .//h2 | .//h3 | .//h4 | .//h5 | .//h6 | .//p | .//li | .//pre")

        parts = []
        for el in text_elements:
            tag = el.tag_name.lower()
            text = el.text.strip()

            if not text or len(text) < 3:
                continue

            if tag == "pre":
                text = text.replace("Copy\n", "").strip()
                parts.append(f"```\n{text}\n```")
            elif tag.startswith("h"):
                level = int(tag[1])
                parts.append(f"{'#' * level} {text}")
            elif tag == "li":
                parts.append(f"- {text}")
            else:
                parts.append(text)

        return "\n\n".join(parts)





















