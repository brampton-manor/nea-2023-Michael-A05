import logging
import time
import psutil

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options

log = logging.getLogger(__name__)


class Scraper:
    def __init__(self, supermarkets, database):
        self.supermarkets = supermarkets
        self.database = database

    def scrape(self) -> None:
        try:
            return self.scrape_cycle()
        except requests.exceptions.Timeout:
            log.warning("Request timed out")
        except requests.exceptions.TooManyRedirects:
            log.warning("Too many redirects")
        except requests.exceptions.RequestException as e:
            log.warning(f"Request except: {e}")
        return None

    def scrape_cycle(self):
        # Indices for accessing category information
        category_id_index = 0
        category_part_url_index = 1
        category_name_index = 2

        # Add supermarkets to the database
        self.database.add_supermarket(self.supermarkets)

        # Iterate over supermarkets and add categories to the database
        for supermarket in self.supermarkets:
            log.info(f"Adding {supermarket.name} categories")
            html = self.get_html(url=supermarket.base_url)
            supermarket_categories = supermarket.filter_categories(html)
            self.database.add_supermarket_category(
                {"supermarket_id": supermarket.get_id(), "supermarket_categories": supermarket_categories}
            )

            # Get the current supermarkets categories and iterate over them
            categories = supermarket.get_categories()
            for category in categories:
                category_name = category[category_name_index]
                # Can select which categories to collect data from by using an if statement here
                wanted_categories = ["bakery", "fresh food", "frozen food", "Bakery & Cakes", "Fresh",
                                     "Frozen", "fresh", "frozen"]

                if category_name in wanted_categories:

                    log.info(f"Retrieving {category_name} products")

                    category_information = supermarket.get_category_information(category_name)
                    start_page_url = supermarket.base_url + category_information[category_part_url_index]
                    page = 1
                    finished_category = False

                    while not finished_category:
                        empty_string = ""
                        url = supermarket.build_url(url=start_page_url, page=page)

                        if url == empty_string:
                            # Get the category products if they are shown on a single page e.g. Morrisons
                            html = self.get_html(url=start_page_url)
                            supermarket_category_products = supermarket.filter_products(html)
                            self.database.add_supermarket_category_products(
                                {"supermarket_category_id": category_information[category_id_index],
                                 "supermarket_category_products": supermarket_category_products}
                            )
                            finished_category = True

                        else:
                            html = self.get_page(url=url)

                            if html is None:
                                finished_category = True
                                log.info(f"Moving to next category")

                            else:
                                # Iterate over the categories pages and get the products
                                supermarket_category_products = supermarket.filter_products(html)
                                self.database.add_supermarket_category_products(
                                    {"supermarket_category_id": category_information[category_id_index],
                                     "supermarket_category_products": supermarket_category_products}
                                )
                                page += 1

                    if finished_category:
                        # Retrieve the products table and query all the products belonging to the current category
                        supermarket_products_table = self.database.get_table_object("supermarket_products")
                        products = self.database.session.query(supermarket_products_table).filter_by(
                            supermarket_category_id=category_information[category_id_index]
                        ).all()

                        # Iterate over each product and extract the products allergen and nutritional information
                        for product in products:
                            product_id, product_part_url = product.id, product.product_part_url

                            # Constructing URL for Morrisons products
                            url = supermarket.base_url.replace("/browse", "") + product_part_url

                            html = self.get_html(url=url)
                            supermarket_product_details = supermarket.filter_product_details(html)

                            if supermarket_product_details is not None:
                                try:
                                    self.database.add_product_information(
                                        {"supermarket_product_id": product_id,
                                         "supermarket_product_details": supermarket_product_details
                                         }
                                    )
                                except KeyError as e:
                                    log.error(f"KeyError processing product {product_id}: {e}. "
                                              f"Details: {supermarket_product_details}")
                                    continue
                                except Exception as ex:
                                    log.error(f"Error processing product {product_id}: {ex}")
                                    continue

                                if "allergens" in supermarket_product_details:
                                    self.database.add_product_allergy_information(
                                        {"supermarket_product_id": product_id,
                                         "supermarket_product_details": supermarket_product_details
                                         }
                                    )
                            else:
                                log.warning(f"{product.product_name} has no nutritional information")
                                continue

    def setup_driver(self):
        user_agent = ("Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                      "Mobile/15E148")

        options = Options()
        options.add_argument("start-maximized")
        options.add_argument("--disable-gpu")
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument(f"user-agent={user_agent}")

        return webdriver.Chrome(options=options)

    def get_html(self, url: str) -> str | None:
        log.info(f"Scraping {url}")
        driver = None
        try:
            driver = self.setup_driver()
            driver.get(url)
            time.sleep(5)
            html = driver.page_source
            return html
        except (WebDriverException, Exception) as e:
            log.error(f"Selenium exception: {e}")
            return None
        finally:
            if driver:
                driver_process = psutil.Process(driver.service.process.pid)
                if driver_process.is_running():
                    driver.close()
                    driver_process.terminate()
                else:
                    log.info("Driver has quit successfully")

    def get_page(self, url: str) -> str | None:
        log.info(f"Scraping {url}")
        driver = None
        try:
            driver = self.setup_driver()
            driver.get(url)
            wait = WebDriverWait(driver, 10)
            element = wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "product-tile"))
            )
            time.sleep(5)
            html = driver.page_source
            return html
        except TimeoutException:
            log.warning(f"Time out waiting for an element")
            return None
        except Exception as e:
            log.error(f"An error occurred while fetching the page: {e}")
            return None
        finally:
            if driver:
                driver_process = psutil.Process(driver.service.process.pid)
                if driver_process.is_running():
                    driver.close()
                    driver_process.terminate()
                else:
                    log.info("Driver has quit successfully")
