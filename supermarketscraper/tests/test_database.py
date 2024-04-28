from unittest import TestCase

from aldi import Aldi
from database import Database


class TestDatabase(TestCase):
    def setUp(self):
        self.db = Database()

    def tearDown(self):
        # Clean up any data added during the test
        self.db.session.rollback()

    def test_add_supermarket(self):
        # Define test supermarket data
        test_supermarket = Aldi()  # Create an instance of the Aldi class
        test_supermarket.id = 1  # Assign an ID for the test supermarket

        # Add the test supermarket to the database
        self.db.add_supermarket([test_supermarket])

        # Retrieve the added supermarket from the database
        supermarkets_table = self.db.get_table_object("supermarkets")
        added_supermarket = self.db.session.query(supermarkets_table).filter_by(supermarket_name="Aldi").first()

        # Assert that the added supermarket exists in the database
        self.assertIsNotNone(added_supermarket, msg="Supermarket should be added to the database")

        # Assert that the added supermarket has correct attributes
        self.assertEqual(test_supermarket.name, added_supermarket.supermarket_name,
                         msg="Supermarket name should match")
        self.assertEqual(test_supermarket.logo, added_supermarket.supermarket_logo,
                         msg="Supermarket logo URL should match")
        self.assertEqual(test_supermarket.base_url, added_supermarket.supermarket_base_url,
                         msg="Supermarket base URL should match")

        # Assert that the ID of the added supermarket is correctly assigned
        self.assertIsNotNone(added_supermarket.id, msg="Supermarket ID should not be None")
        self.assertEqual(test_supermarket.id, added_supermarket.id, msg="Supermarket ID should match")

    def test_add_supermarket_category(self):
        # Define test data for supermarket categories
        test_categories_data = [
            {'name': 'Specially Selected', 'part_url': '/en-GB/specially-selected?'},
            {'name': 'Vegan & Plant Based', 'part_url': '/en-GB/vegan-range?'},
            {'name': 'Bakery', 'part_url': '/en-GB/bakery?'}
        ]

        # Add the test categories to the database
        self.db.add_supermarket_category({"supermarket_id": 1, "supermarket_categories": test_categories_data})

        # Retrieve the added categories from the database
        supermarket_categories_table = self.db.get_table_object("supermarket_categories")
        added_categories = self.db.session.query(supermarket_categories_table).all()

        # Assert that the correct number of categories were added to the database
        self.assertEqual(len(test_categories_data), len(added_categories),
                         msg="Number of added categories should match")

        # Assert that each category was added correctly
        for test_category, added_category in zip(test_categories_data, added_categories):
            self.assertEqual(test_category['name'], added_category.supermarket_category_name,
                             msg="Category name should match")
            self.assertEqual(test_category['part_url'], added_category.supermarket_category_part_url,
                             msg="Category part URL should match")

    def test_add_supermarket_product(self):
        # Define test data for supermarket products
        test_products_data = [
            {'name': 'Organic Bread', 'price': 2.99, 'image': 'bread.jpg', 'part_url': '/en-GB/organic-bread'},
            {'name': 'Vegan Burger', 'price': 4.49, 'image': 'burger.jpg', 'part_url': '/en-GB/vegan-burger'},
            {'name': 'Gluten-Free Pasta', 'price': 3.79, 'image': 'pasta.jpg', 'part_url': '/en-GB/gluten-free-pasta'}
        ]

        # Add the test products to the database
        self.db.add_supermarket_category_products(
            {"supermarket_category_id": 1, "supermarket_category_products": test_products_data})

        # Retrieve the added products from the database
        supermarket_products_table = self.db.get_table_object("supermarket_products")
        added_products = self.db.session.query(supermarket_products_table).all()

        # Assert that the correct number of products were added to the database
        self.assertEqual(len(test_products_data), len(added_products),
                         msg="Number of added products should match")

        # Assert that each product was added correctly
        for test_product, added_product in zip(test_products_data, added_products):
            self.assertEqual(test_product['name'], added_product.product_name,
                             msg="Product name should match")
            self.assertEqual(test_product['price'], added_product.product_price,
                             msg="Product price should match")
            self.assertEqual(test_product['image'], added_product.product_image,
                             msg="Product image URL should match")
            self.assertEqual(test_product['part_url'], added_product.product_part_url,
                             msg="Product part URL should match")

    def test_add_product_details(self):
        # Define test data for product details
        test_details_data = {
            'energy_kj': 1500.0,
            'energy_kcal': 350.0,
            'fat': 10.5,
            'of_which_saturates': 3.2,
            'carbohydrates': 50.0,
            'of_which_sugars': 5.0,
            'fibre': 3.0,
            'protein': 15.0,
            'salt': 1.2
        }

        # Add the test product details to the database
        self.db.add_product_information({"supermarket_product_id": 1, "supermarket_product_details": test_details_data})

        # Retrieve the added product details from the database
        supermarket_product_details_table = self.db.get_table_object("supermarket_product_details")
        added_details = self.db.session.query(supermarket_product_details_table).filter_by(
            supermarket_product_id=1).first()

        # Assert that the added product details exist in the database
        self.assertIsNotNone(added_details, msg="Product details should be added to the database")

        # Assert that the added product details match the test data
        self.assertEqual(test_details_data['energy_kj'], added_details.energy_kj,
                         msg="Energy (kJ) should match")
        self.assertEqual(test_details_data['energy_kcal'], added_details.energy_kcal,
                         msg="Energy (kcal) should match")
        self.assertEqual(test_details_data['fat'], added_details.fat,
                         msg="Fat should match")
        self.assertEqual(test_details_data['of_which_saturates'], added_details.of_which_saturates,
                         msg="Saturates should match")
        self.assertEqual(test_details_data['carbohydrates'], added_details.carbohydrates,
                         msg="Carbohydrates should match")
        self.assertEqual(test_details_data['of_which_sugars'], added_details.of_which_sugars,
                         msg="Sugars should match")
        self.assertEqual(test_details_data['fibre'], added_details.fibre,
                         msg="Fibre should match")
        self.assertEqual(test_details_data['protein'], added_details.protein,
                         msg="Protein should match")
        self.assertEqual(test_details_data['salt'], added_details.salt,
                         msg="Salt should match")

    def test_add_product_allergens(self):
        # Define test data for product allergens
        test_allergens_data = ['wheat', 'soy', 'milk']

        # Add the test product allergens to the database
        self.db.add_product_allergy_information(
            {"supermarket_product_id": 1, "supermarket_product_details": {"allergens": test_allergens_data}})

        # Retrieve the added product allergens from the database
        supermarket_product_allergens_table = self.db.get_table_object("supermarket_product_allergens")
        added_allergens = self.db.session.query(supermarket_product_allergens_table).filter_by(
            supermarket_product_id=1).all()

        # Assert that the correct number of allergens were added to the database
        self.assertEqual(len(test_allergens_data), len(added_allergens))