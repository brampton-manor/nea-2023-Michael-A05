import logging
import re

import sqlalchemy.sql.schema

from database import Database

db = Database()
log = logging.getLogger(__name__)


class Supermarkets:
    def __init__(self):
        # Initialise instance variables
        self.name = ""
        self.logo = ""
        self.base_url = ""
        self.id = None
        self.categories = self.get_categories()
        self.allergens = self.get_allergens()
        self.nutrition_pattern = self.get_nutrition_pattern()

    def build_url(self, url: str, page: int) -> str:
        # Abstract method to build a URL for a specific page
        return ""

    def filter_categories(self, html: str | None) -> list:
        # Abstract method to filter supermarket categories from HTML content
        return []

    def filter_products(self, html: str | None) -> list:
        # Abstract method to filter supermarket products from HTML content
        return []

    def filter_product_details(self, html: str | None) -> dict:
        # Abstract method to filter products from HTML content
        return {}

    def assign_product_values(self, nutritional_values: list, allergens: list) -> dict | None:
        # Method to assign the values of a products nutritional information
        product_details = {}

        try:
            energy_kj, energy_kcal, fat, sat_fat, carb, sugars, fibre, protein, salt = nutritional_values
            product_details['energy_kj'] = float(energy_kj)
            product_details['energy_kcal'] = float(energy_kcal)
            product_details['fat'] = float(fat)
            product_details['of_which_saturates'] = float(sat_fat)
            product_details['carbohydrates'] = float(carb)
            product_details['of_which_sugars'] = float(sugars)
            product_details['fibre'] = float(fibre)
            product_details['protein'] = float(protein)
            product_details['salt'] = float(salt)
            product_details['allergens'] = list(allergens)

            return product_details

        except ValueError as e:
            log.error(f"Error processing nutritional values: {e}")
            return None

        except Exception as ex:
            log.error(f"An error occurred while trying to process product details for a {self.name} product: {ex}")
            return None

    def assign_default_values(self, allergens: list) -> dict:
        # Method to assign default values for a products nutritional information if the data wasn't available
        log.info(f"Assigning default values")
        product_details = {'energy_kj': 0.0, 'energy_kcal': 0.0, 'fat': 0.0, 'of_which_saturates': 0.0,
                           'carbohydrates': 0.0, 'of_which_sugars': 0.0, 'fibre': 0.0, 'protein': 0.0, 'salt': 0.0,
                           'allergens': allergens}
        return product_details

    def format_product_image_src(self, src: str) -> str:
        # Method to format product image source URLs
        return src.replace("\\\\", "/").replace("\\", "/")

    def format_product_price_pence(self, price_string: str) -> float:
        # Method to format the prices of products where the respective string contains a pence symbol
        return float(price_string.replace("p", ""))

    def format_product_price_pound(self, price_string: str) -> float:
        # Method to format the prices of products where the respective string contains a pound symbol
        return float(price_string.replace("£", ""))

    def format_supermarket_category_products(self, product_list: list) -> list:
        # Method to format supermarket product information
        for product in product_list:
            try:
                product.update({'image': self.format_product_image_src(product['image'])})
            except KeyError:
                log.warning(f"Product {product['name']} has no image")
                continue
        return product_list

    def format_nutritional_information(self, nutrition_text: str) -> list:
        # Abstract method to format supermarket product nutritional information
        return ['0', '0', '0', '0', '0', '0', '0', '0', '0']

    def get_id(self) -> int | None:
        # Method to get the ID of a supermarket from the database
        try:
            supermarket_object = db.get_table_object("supermarkets")
            row = db.session.query(supermarket_object).filter_by(supermarket_name=self.name).first()
            if row:
                return row.id
            else:
                return None
        except Exception as e:
            log.error(f"Error retrieving ID for {self.name}: {e}")
            return None

    def get_categories(self) -> sqlalchemy.sql.schema.Table | list:
        # Method to get the categories of a supermarket
        try:
            supermarket_id = self.get_id()
            if supermarket_id is not None:
                supermarket_categories_object = db.get_table_object("supermarket_categories")
                return db.session.query(supermarket_categories_object).filter_by(supermarket_id=supermarket_id).all()
            else:
                log.info("Supermarket ID not found")
                return []
        except Exception as e:
            log.exception(f"Error retrieving categories for {self.name}: {e}")
            return []

    def get_category_information(self, category_name: str) -> tuple:
        # Method to get the ID and part-URL for specific categories
        try:
            supermarket_categories_object = db.get_table_object("supermarket_categories")
            row = db.session.query(supermarket_categories_object).filter_by(
                supermarket_category_name=category_name).first()
            if row:
                category_id = row.id
                category_part_url = row.supermarket_category_part_url
                return category_id, category_part_url
            else:
                log.warning(f"{category_name} category not found")
                return None, None
        except Exception as e:
            log.exception(f"Error retrieving category information for '{category_name}': {e}")
            return None, None

    def get_allergens(self) -> list:
        # Method to get a list of common food allergens
        return [
            "peanuts", "almonds", "walnuts", "cashews", "pistachios", "milk", "eggs", "wheat", "barley", "soya",
            "mustard", "lupin", "rye", "sulphites", "fish", "shellfish", "celery", "sesame", "molluscs"
        ]

    def get_nutrition_pattern(self) -> str:
        # Abstract method representing the regular expressions used to extract values from nutritional information
        return r""
