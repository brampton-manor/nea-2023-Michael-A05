import logging

from bs4 import BeautifulSoup
from scraper import Scraper

log = logging.getLogger(__name__)


class Tesco:
    def __init__(self) -> None:
        self.name = "Tesco"
        self.base_url = f"https://www.tesco.com/groceries/"
        self.start_page = 1
        log.info(f"{self.name} loaded")

    def build_url(self, page):
        return self.base_url + f"page={self.start_page + page}&count=48"

    def return_supermarket_categories(self, html):
        soup = BeautifulSoup(html, "html.parser")
        supermarket_categories = []



    def return_stock_names(self, html):
        soup = BeautifulSoup(html, "html.parser")
        stock_names = []
        try:
            for litag in soup.find_all('li', {'class': 'product-list--list-item'}):
                for stock_name in litag.find('span', {'class': 'ddsweb-link__text'}):
                    stock_names.append(stock_name)
        except TypeError as e:
            log.error(f"Filter type exception: {e}")
        except Exception as e:
            log.error(f"Filter exception: {e}")
        return stock_names

    def return_stock_prices(self, html):
        soup = BeautifulSoup(html, "html.parser")
        stock_prices = []
        try:
            for litag in soup.find_all('li', {'class': 'product-list--list-item'}):
                for stock_price in litag.find('p', {'class': 'beans-price__text'}):
                    chr_to_remove = "£"
                    stock_price = stock_price.replace(chr_to_remove, "")
                    stock_prices.append(stock_price)
        except TypeError as e:
            log.error(f"Filter type exception: {e}")
        except Exception as e:
            log.error(f"Filter exception: {e}")
        return stock_prices

    def return_stock_images(self, html):
        soup = BeautifulSoup(html, "html.parser")
        stock_images = []
        try:
            for litag in soup.find_all('li', {'class': 'product-list--list-item'}):
                for stock_image in litag.find_all('img'):
                    stock_images.append(stock_image.get('src'))
        except TypeError as e:
            log.error(f"Filter type exception: {e}")
        except Exception as e:
            log.error(f"Filter exception: {e}")
        return stock_images

    def return_stock_part_urls(self, html):
        soup = BeautifulSoup(html, "html.parser")
        stock_part_urls = []
        try:
            for litag in soup.find_all('li', {'class': 'product-list--list-item'}):
                for stock_part_url in litag.find_all('a', href=True):
                    if "/groceries" in stock_part_url.get('href'):
                        stock_part_urls.append(stock_part_url.get('href'))
        except TypeError as e:
            log.error(f"Filter type exception: {e}")
        except Exception as e:
            log.error(f"Filter exception: {e}")
        return stock_part_urls

    def filter_stock(self, html):
        stock_details = []
        soup = BeautifulSoup(html, "html.parser")

        try:
            for litag in soup.find_all('li', {'class': 'product-list--list-item'}):
                stock = {}
                for stock_name in litag.find('span', {'class': 'ddsweb-link__text'}):
                    stock["name"] = stock_name
                for stock_price in litag.find('p', {'class': 'beans-price__text'}):
                    chr_to_remove = "£"
                    stock_price = stock_price.replace(chr_to_remove, "")
                    stock["price"] = stock_price
                for stock_image in litag.find_all('img'):
                    stock["image"] = stock_image.get('src')
                for stock_part_url in litag.find_all('a', href=True):
                    if "/groceries" in stock_part_url.get('href'):
                        stock["part_url"] = stock_part_url.get('href')
                stock_details.append(stock)
        except TypeError as e:
            log.error(f"Filter type exception: {e}")
        except Exception as e:
            log.error(f"Filter exception: {e}")
        return stock_details


"""
tesco = Tesco()
scraper = Scraper(tesco)

html = scraper.get_html(tesco.url)
stock_details = tesco.filter(html)
print(stock_details)
"""