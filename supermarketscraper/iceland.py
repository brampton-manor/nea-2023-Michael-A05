import logging

from bs4 import BeautifulSoup
from supermarkets import Supermarkets

log = logging.getLogger(__name__)


class Iceland(Supermarkets):

    def __init__(self):
        super().__init__()
        self.name = "Iceland"
        self.logo = ("https://www.bing.com/th?id=OIP.nn40kuPZtVCz-7QNSxbVUwHaHa&w=101&h=100&c=8&rs=1&qlt=90&o=6&pid=3"
                     ".1&rm=2")
        self.base_url = "https://www.iceland.co.uk/"

    def build_url(self, url, page):
        multiplier = 25
        return url + f"?start={page * multiplier}"

    def filter_categories(self, html):
        if html is not None:

            soup = BeautifulSoup(html, "html.parser")
            supermarket_categories = []

            try:

                for a_tag in soup.find_all('a', {'class': 'menu-sub-cat-link viewall'}):
                    hyperlink_string = a_tag.get('href')
                    category = {'name': hyperlink_string.replace(self.base_url, ""),
                                'part_url': hyperlink_string.replace(self.base_url, "")}

                    supermarket_categories.append(category)

                return supermarket_categories
            except Exception as e:
                log.error(f"Error filtering {self.name} categories: {e}")
                return []
        else:
            log.error(f"Page was not found: category html for {self.name} was not passed correctly")
            return []

    def filter_products(self, html):
        if html is not None:
            soup = BeautifulSoup(html, "html.parser")
            supermarket_category_products = []

            try:
                for divtag in soup.find_all('div', {'class': 'product-tile'}):
                    product = {}
                    for product_name in divtag.find('a', {'class': 'name-link'}):
                        if product_name.string != '\n':
                            product['name'] = product_name.string
                    for product_price in divtag.find('span', {'class': 'product-sales-price'}):
                        if product_price.get_text(strip=True) != '':
                            product_price = self.format_product_price_pound(product_price.get_text())
                            product['price'] = product_price
                    for product_part_url in divtag.find_all('a', {'class': 'name-link'}):
                        product['part_url'] = product_part_url.get('href').replace(self.base_url, "")
                    for product_image in divtag.find_all('img'):                # error here, iceland uses lazy loading
                        product['image'] = product_image.get('src')
                    supermarket_category_products.append(product)
                return supermarket_category_products
            except Exception as e:
                log.error(f"Error filtering products for {self.name}: {e}")
                return []
        else:
            log.error(f"Page was not found: product html for {self.name} was not passed correctly")
            return []

from scraper import Scraper

scraper = Scraper(supermarkets=None, database=None)
iceland = Iceland()
url = "https://www.iceland.co.uk/frozen"
html = scraper.get_html(url)
iceland.filter_categories(html)
x = iceland.filter_categories(html)
print(x)
