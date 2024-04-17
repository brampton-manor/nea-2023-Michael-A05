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
                    for product_image in divtag.find_all('img'):  # error here, iceland uses lazy loading
                        product['image'] = product_image.get('src')
                    supermarket_category_products.append(product)
                return supermarket_category_products
            except Exception as e:
                log.error(f"Error filtering products for {self.name}: {e}")
                return []
        else:
            log.error(f"Page was not found: product html for {self.name} was not passed correctly")
            return []

    def filter_product_details(self, html):
        if html is not None:

            soup = BeautifulSoup(html, "html.parser")
            allergy_list = []

            try:
                divtag = soup.find('div', {'class': 'mt-3'})
                for ptag in divtag.find_all('p', {'class': 'text-muted'}):
                    allergen_text = ptag.get_text(strip=True)
                    for allergen in self.allergens:
                        if allergen_text.lower().find(allergen) >= 0:
                            allergy_list.append(allergen)

                    allergy_list = list(set(allergy_list))

                nutrition_table = soup.find('tbody')
                nutritional_values = []
                for row in nutrition_table.find_all('tr'):
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        #   nutrient = cols[0].get_text(strip=True)
                        value_per_100g = cols[2].get_text(strip=True)
                        if value_per_100g != '':
                            nutritional_values.append(value_per_100g)
                nutritional_values = self.format_nutritional_information(nutritional_values)
                product_details = self.assign_product_values(nutritional_values, allergy_list)
                if product_details is None:
                    product_details = self.assign_default_values(allergy_list)

                return product_details if product_details else None

            except Exception as e:
                log.error(f"Error filtering product details for {self.name}: {e}")
                return None
        else:
            log.error(f"Page was not found: product information html for {self.name} was not passed correctly")
            return None

    def format_nutritional_information(self, values):
        try:
            formatted_values = [values[0].replace("kJ", ""), values[1].replace("kcal", "")]
            for value in values[2:]:
                formatted_values.append(value.replace("g", ""))
            return formatted_values

        except Exception as e:
            log.error(f"Error formatting values: {e}")
            formatted_values = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
            return formatted_values

