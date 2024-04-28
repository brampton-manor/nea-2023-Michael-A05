import logging
import unicodedata
import re

from bs4 import BeautifulSoup
from supermarkets import Supermarkets

log = logging.getLogger(__name__)


class Aldi(Supermarkets):
    def __init__(self):
        # Initialise Aldi-specific attributes
        super().__init__()
        self.name = "Aldi"
        self.logo = "https://cdn.aldi-digital.co.uk/32FDVWu4Lhbxgj9Z3v03ji0pGJIp?&w=70&h=84"
        self.base_url = "https://groceries.aldi.co.uk"
        log.info(f"{self.name} loaded")

    def build_url(self, url: str, page: int) -> str:
        return url + f"&page={page}"

    def filter_categories(self, html: str | None) -> list:
        if html is not None:
            soup = BeautifulSoup(html, "html.parser")
            supermarket_categories = []

            try:
                for litag in soup.find_all('li', {'class': 'submenu'}):
                    category = {}

                    # Extract category name
                    for category_name in litag.find('a', {'class': 'dropdown-item'}):
                        if 'SHOP ALL' in category_name:
                            category_name = category_name[9:].lower()
                            category['name'] = category_name.strip()

                    # Extract category part-URL
                    for category_part_url in litag.find_all('a', href=True):
                        if 'shopall' in category_part_url.get('href'):
                            hyperlink_string = category_part_url.get('href')
                            length = hyperlink_string.find("?")
                            category['part_url'] = hyperlink_string[:length + 1]

                    supermarket_categories.append(category)

                supermarket_categories = [dictionary for dictionary in supermarket_categories if dictionary]
                return supermarket_categories

            except Exception as e:
                log.error(f"Error filtering {self.name} categories: {e}")
                return []
        else:
            log.error(f"Page was not found: category html for {self.name} was not passed correctly")
            return []

    def filter_products(self, html: str | None) -> list:
        if html is not None:
            soup = BeautifulSoup(html, "html.parser")
            supermarket_category_products = []

            try:
                for divtag in soup.find_all('div', {'class': 'product-tile'}):
                    product = {}

                    # Extract product name
                    for product_name in divtag.find('a', {'class': 'p text-default-font'}):
                        product['name'] = product_name

                    # Extract product price
                    for product_price in divtag.find('span', {'class': 'h4'}):
                        product['price'] = self.format_product_price_pound(product_price.string)

                    # Extract product part-URL
                    for product_part_url in divtag.find('div', 'image-tile'):
                        try:
                            product_part_url = product_part_url.get('href')
                            if product_part_url is not None:
                                product['part_url'] = product_part_url
                        except AttributeError as e:
                            log.warning(f"Error filtering part_url for {product['name']}: {e}")
                            continue

                    # Extract product image
                    for product_image in divtag.find('figure'):
                        product['image'] = product_image.get('src')

                    supermarket_category_products.append(product)

                return self.format_supermarket_category_products(supermarket_category_products)

            except Exception as e:
                log.error(f"Error filtering products for {self.name}: {e}")
                return []
        else:
            log.error(f"Page was not found: product html for {self.name} was not passed correctly")
            return []

    def filter_product_details(self, html: str | None) -> dict | None:
        if html is not None:
            soup = BeautifulSoup(html, "html.parser")
            allergy_list = []

            try:
                for table_row in soup.find('tbody'):

                    # Extract product allergens
                    if "Ingredients" in table_row.get_text():
                        ingredients_text = table_row.get_text().replace("Ingredients", "").strip()
                        ingredients_text = unicodedata.normalize("NFKC", ingredients_text)
                        for allergen in self.get_allergens():
                            if ingredients_text.lower().find(allergen) >= 0:
                                allergy_list.append(allergen)

                    if "Allergy advice" in table_row.get_text():
                        allergy_text = table_row.get_text().replace("Allergy advice", "").strip()
                        for allergen in self.get_allergens():
                            if allergy_text.lower().find(allergen) >= 0:
                                allergy_list.append(allergen)
                        allergy_list = list(set(allergy_list))

                    # Extract product nutritional values
                    if "Nutrition information" in table_row.get_text():
                        nutrition_text = table_row.get_text().replace("Nutrition information", "").strip()
                        values = self.format_nutritional_information(nutrition_text)
                        product_details = self.assign_product_values(values, allergy_list)
                        if product_details is None:
                            product_details = self.assign_default_values(allergy_list)

                        return product_details if product_details else None

            except Exception as e:
                log.error(f"Error filtering product details for {self.name}: {e}")
                return None
        else:
            log.error(f"Page was not found: product information html for {self.name} was not passed correctly")
            return None

    def format_nutritional_information(self, nutrition_text: str) -> list:
        # List to store formatted nutritional values
        formatted_values = []
        # Extract matches from the nutrition text using a regular expression
        matches = re.findall(self.nutrition_pattern, nutrition_text)

        if matches:
            # Check if the number of matches is valid
            if len(matches) == 2 or len(matches) == 9:
                # Define nutritional labels
                nutritional_labels = ["energy_kj", "energy_kcal", "fat", "fat_sat", "carb", "sugars", "fibre",
                                      "protein",
                                      "salt"]
                # Default value for missing nutritional information
                default_value = 0

                for label in nutritional_labels:
                    # Check if the label is for energy (kJ or kcal)
                    if label == "energy_kj" or label == "energy_kcal":
                        try:
                            value = matches[nutritional_labels.index(label)][2].lower()

                            if value == '':
                                # Log a warning if the value is empty
                                log.warning(
                                    f"Value for {nutritional_labels[nutritional_labels.index(label) + 1]} may be "
                                    f"incorrect")
                                raise ValueError

                            else:
                                # Format the value and add it to the list of nutritional information
                                formatted_value = str(value).replace("<", "").strip()
                                formatted_value = formatted_value.replace(".", "").strip()
                                formatted_value = formatted_value.replace("kj", "")
                                formatted_value = formatted_value.replace("kcal", "")
                                formatted_values.append(formatted_value)

                        except ValueError:
                            log.error(f"Value not found for {label}, setting default value.")
                            formatted_values.append(str(default_value))
                    else:
                        try:
                            # Extract the value for the current label then format it and add it to the list
                            value = matches[nutritional_labels.index(label)][1]
                            formatted_value = str(value).replace("<", "").strip()
                            formatted_values.append(formatted_value)
                        except IndexError:
                            # Log an error if any values aren't found and set default values
                            log.error(f"Value not found for {label}, setting default value.")
                            formatted_values.append(str(default_value))
            else:
                # Log a warning if the nutritional information format is invalid and set default values
                log.warning("Nutritional information was not in valid format")
                formatted_values = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        else:
            # Log a warning if no matches are found and set default values
            log.warning("Match was not found")
            formatted_values = ['0', '0', '0', '0', '0', '0', '0', '0', '0']

        return formatted_values

    def get_nutrition_pattern(self) -> str:
        # Regular expression pattern to match nutritional information
        return (r"(Fat|of which saturates|Carbohydrate|of which sugars|Fibre|Protein|Salt)(\s+[<]?\d+[.]?\d+|\s+\d+)|("
                r"\d+[.]?[kK][jJ]|\d+[.]?kcal)")
