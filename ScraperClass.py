#imports:
import logging
import requests  # type: ignore
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
import urllib
import time


log = logging.getLogger(__name__)


class Scraper:

    def __init__(self) -> None:
        pass

    def scrape(self):
        try:
            self.scrape_cycle()

        except requests.exceptions.Timeout:
            log.warning("Request timed out")

        except requests.exceptions.TooManyRedirects:
            log.warning("Too many redirects")

        except requests.exceptions.RequestException as e:
            log.warning(f"Request except: {e}")

    def scrape_cycle(self, page):
        log.info("Scraper starting")

        try:
            chromedriver_autoinstaller.install()

        except urllib.error.URLError as e:
            log.error(f"Error with chromedriver auto-installation - {e}")
            return ""

        user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"

        options = Options()
        options.headless = True
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument(f"user-agent={user_agent}")

        try:
            driver = webdriver.Chrome(options=options)
            driver.get(f"https://www.iceland.co.uk/fresh?start={page}") #edit later to automate switching websites and incrementing page

        except WebDriverException as e:
            log.error(f"Selenium exception: {e.msg}")
            return ""

        time.sleep(1)

        html = driver.page_source
        driver.quit()
        return html
