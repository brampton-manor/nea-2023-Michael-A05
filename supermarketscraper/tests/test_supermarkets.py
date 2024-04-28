from unittest import TestCase
from unittest.mock import MagicMock
from supermarkets import Supermarkets
from database import Database


class TestSupermarkets(TestCase):
    def setUp(self):
        self.supermarkets = Supermarkets()
        self.database = Database()

    def test_build_url_with_page_1(self):
        # Test build_url method with page 1
        url = self.supermarkets.build_url("https://example.com", 1)
        self.assertEqual("", url)

    def test_build_url_with_empty_url(self):
        # Test build_url method with empty URL
        url = self.supermarkets.build_url("", 1)
        self.assertEqual("", url)

    def test_build_url_with_negative_page(self):
        # Test build_url method with negative page number
        url = self.supermarkets.build_url("https://example.com", -1)
        self.assertEqual("", url)

    def test_build_url_with_invalid_url(self):
        # Test build_url method with invalid URL
        url = self.supermarkets.build_url("invalid_url", 1)
        self.assertEqual("", url)

    def test_filter_categories_with_valid_html(self):
        # Test filter_categories method with valid HTML containing categories
        html = "<div class='category'>Category 1</div><div class='category'>Category 2</div>"
        categories = self.supermarkets.filter_categories(html)
        self.assertEqual([], categories)

    def test_filter_categories_with_empty_html(self):
        # Test filter_categories method with empty HTML
        html = ""
        categories = self.supermarkets.filter_categories(html)
        self.assertEqual([], categories)

    def test_filter_categories_with_none_html(self):
        # Test filter_categories method with None HTML
        categories = self.supermarkets.filter_categories(None)
        self.assertEqual([], categories)

    def test_filter_categories_with_invalid_html(self):
        # Test filter_categories method with invalid HTML
        html = "<div>Category 1</div><div>Category 2</div>"
        categories = self.supermarkets.filter_categories(html)
        self.assertEqual([], categories)

    def test_filter_categories_with_html_missing_category_class(self):
        # Test filter_categories method with HTML missing category class
        html = "<div>Category 1</div><div>Category 2</div>"
        categories = self.supermarkets.filter_categories(html)
        self.assertEqual([], categories)

    def test_filter_products_with_valid_html(self):
        # Test filter_products method with valid HTML containing products
        html = "<div class='product'>Product 1</div><div class='product'>Product 2</div>"
        products = self.supermarkets.filter_products(html)
        self.assertEqual([], products)

    def test_filter_products_with_empty_html(self):
        # Test filter_products method with empty HTML
        html = ""
        products = self.supermarkets.filter_products(html)
        self.assertEqual([], products)

    def test_filter_products_with_none_html(self):
        # Test filter_products method with None HTML
        products = self.supermarkets.filter_products(None)
        self.assertEqual([], products)

    def test_filter_products_with_invalid_html(self):
        # Test filter_products method with invalid HTML
        html = "<div>Product 1</div><div>Product 2</div>"
        products = self.supermarkets.filter_products(html)
        self.assertEqual([], products)

    def test_filter_products_with_html_missing_product_class(self):
        # Test filter_products method with HTML missing product class
        html = "<div>Product 1</div><div>Product 2</div>"
        products = self.supermarkets.filter_products(html)
        self.assertEqual([], products)

    def test_filter_product_details_with_valid_html(self):
        # Test filter_product_details method with valid HTML containing product details
        html = "<div class='product-details'>Details</div>"
        product_details = self.supermarkets.filter_product_details(html)
        self.assertEqual({}, product_details)

    def test_filter_product_details_with_empty_html(self):
        # Test filter_product_details method with empty HTML
        html = ""
        product_details = self.supermarkets.filter_product_details(html)
        self.assertEqual({}, product_details)

    def test_filter_product_details_with_none_html(self):
        # Test filter_product_details method with None HTML
        product_details = self.supermarkets.filter_product_details(None)
        self.assertEqual({}, product_details)

    def test_filter_product_details_with_invalid_html(self):
        # Test filter_product_details method with invalid HTML
        html = "<div>Details</div>"
        product_details = self.supermarkets.filter_product_details(html)
        self.assertEqual({}, product_details)

    def test_filter_product_details_with_html_missing_details_class(self):
        # Test filter_product_details method with HTML missing product details class
        html = "<div>Details</div>"
        product_details = self.supermarkets.filter_product_details(html)
        self.assertEqual({}, product_details)

    def test_assign_product_values_with_valid_values(self):
        # Test assign_product_values method with valid nutritional values
        nutritional_values = ['100', '200', '10', '5', '20', '15', '3', '15', '1']
        allergens = ['peanuts', 'milk']
        product_details = self.supermarkets.assign_product_values(nutritional_values, allergens)
        self.assertEqual({
            'energy_kj': 100.0,
            'energy_kcal': 200.0,
            'fat': 10.0,
            'of_which_saturates': 5.0,
            'carbohydrates': 20.0,
            'of_which_sugars': 15.0,
            'fibre': 3.0,
            'protein': 15.0,
            'salt': 1.0,
            'allergens': ['peanuts', 'milk']
        }, product_details)

    def test_assign_product_values_with_invalid_values(self):
        # Test assign_product_values method with invalid nutritional values
        nutritional_values = ['100', '200', 'invalid', '5', '20', '15', '3', '15', '1']
        allergens = ['peanuts', 'milk']
        product_details = self.supermarkets.assign_product_values(nutritional_values, allergens)
        self.assertIsNone(product_details)

    def test_assign_product_values_with_missing_values(self):
        # Test assign_product_values method with missing nutritional values
        nutritional_values = ['100', '200', '10', '5', '20', '15']
        allergens = ['peanuts', 'milk']
        product_details = self.supermarkets.assign_product_values(nutritional_values, allergens)
        self.assertIsNone(product_details)

    def test_assign_product_values_with_empty_values(self):
        # Test assign_product_values method with empty nutritional values
        nutritional_values = []
        allergens = ['peanuts', 'milk']
        product_details = self.supermarkets.assign_product_values(nutritional_values, allergens)
        self.assertIsNone(product_details)

    def test_assign_product_values_with_invalid_allergens(self):
        # Test assign_product_values method with invalid allergens
        nutritional_values = ['100', '200', '10', '5', '20', '15', '3', '15', '1']
        allergens = ['invalid']
        product_details = self.supermarkets.assign_product_values(nutritional_values, allergens)
        self.assertEqual(product_details, {
            'energy_kj': 100.0,
            'energy_kcal': 200.0,
            'fat': 10.0,
            'of_which_saturates': 5.0,
            'carbohydrates': 20.0,
            'of_which_sugars': 15.0,
            'fibre': 3.0,
            'protein': 15.0,
            'salt': 1.0,
            'allergens': ['invalid']
        })

    def test_assign_product_values_with_empty_allergens(self):
        # Test assign_product_values method with empty allergens
        nutritional_values = ['100', '200', '10', '5', '20', '15', '3', '15', '1']
        allergens = []
        product_details = self.supermarkets.assign_product_values(nutritional_values, allergens)
        self.assertEqual({
            'energy_kj': 100.0,
            'energy_kcal': 200.0,
            'fat': 10.0,
            'of_which_saturates': 5.0,
            'carbohydrates': 20.0,
            'of_which_sugars': 15.0,
            'fibre': 3.0,
            'protein': 15.0,
            'salt': 1.0,
            'allergens': []
        }, product_details)

    def test_assign_product_values_with_invalid_values_and_allergens(self):
        # Test assign_product_values method with invalid nutritional values and allergens
        nutritional_values = ['100', '200', 'invalid', '5', '20', '15', '3', '15', '1']
        allergens = ['invalid']
        product_details = self.supermarkets.assign_product_values(nutritional_values, allergens)
        self.assertIsNone(product_details)

    def test_assign_product_values_with_empty_values_and_allergens(self):
        # Test assign_product_values method with empty nutritional values and allergens
        nutritional_values = []
        allergens = []
        product_details = self.supermarkets.assign_product_values(nutritional_values, allergens)
        self.assertIsNone(product_details)

    def test_assign_default_values_with_allergens(self):
        # Test assign_default_values method with allergens provided
        allergens = ['peanuts', 'milk']
        product_details = self.supermarkets.assign_default_values(allergens)
        expected_product_details = {
            'energy_kj': 0.0,
            'energy_kcal': 0.0,
            'fat': 0.0,
            'of_which_saturates': 0.0,
            'carbohydrates': 0.0,
            'of_which_sugars': 0.0,
            'fibre': 0.0,
            'protein': 0.0,
            'salt': 0.0,
            'allergens': ['peanuts', 'milk']
        }
        self.assertEqual(expected_product_details, product_details)

    def test_assign_default_values_without_allergens(self):
        # Test assign_default_values method without allergens provided
        product_details = self.supermarkets.assign_default_values([])
        expected_product_details = {
            'energy_kj': 0.0,
            'energy_kcal': 0.0,
            'fat': 0.0,
            'of_which_saturates': 0.0,
            'carbohydrates': 0.0,
            'of_which_sugars': 0.0,
            'fibre': 0.0,
            'protein': 0.0,
            'salt': 0.0,
            'allergens': []
        }
        self.assertEqual(expected_product_details, product_details)

    def test_assign_default_values_with_invalid_allergens(self):
        # Test assign_default_values method with invalid allergens
        allergens = ['invalid']
        product_details = self.supermarkets.assign_default_values(allergens)
        expected_product_details = {
            'energy_kj': 0.0,
            'energy_kcal': 0.0,
            'fat': 0.0,
            'of_which_saturates': 0.0,
            'carbohydrates': 0.0,
            'of_which_sugars': 0.0,
            'fibre': 0.0,
            'protein': 0.0,
            'salt': 0.0,
            'allergens': ['invalid']
        }
        self.assertEqual(expected_product_details, product_details)

    def test_assign_default_values_with_none_allergens(self):
        # Test assign_default_values method with None allergens
        product_details = self.supermarkets.assign_default_values(None)
        expected_product_details = {
            'energy_kj': 0.0,
            'energy_kcal': 0.0,
            'fat': 0.0,
            'of_which_saturates': 0.0,
            'carbohydrates': 0.0,
            'of_which_sugars': 0.0,
            'fibre': 0.0,
            'protein': 0.0,
            'salt': 0.0,
            'allergens': None
        }
        self.assertEqual(expected_product_details, product_details)

    def test_assign_default_values_with_mixed_type_allergens(self):
        # Test assign_default_values method with mixed type allergens
        allergens = [None, 1, 'peanuts']
        product_details = self.supermarkets.assign_default_values(allergens)
        expected_product_details = {
            'energy_kj': 0.0,
            'energy_kcal': 0.0,
            'fat': 0.0,
            'of_which_saturates': 0.0,
            'carbohydrates': 0.0,
            'of_which_sugars': 0.0,
            'fibre': 0.0,
            'protein': 0.0,
            'salt': 0.0,
            'allergens': [None, 1, 'peanuts']
        }
        self.assertEqual(product_details, expected_product_details)

    def test_format_product_image_src_with_backslashes(self):
        # Test format_product_image_src method with backslashes in the source URL
        src = "path\\to\\image.jpg"
        formatted_src = self.supermarkets.format_product_image_src(src)
        self.assertEqual(formatted_src, "path/to/image.jpg")

    def test_format_product_image_src_without_backslashes(self):
        # Test format_product_image_src method without backslashes in the source URL
        src = "path/to/image.jpg"
        formatted_src = self.supermarkets.format_product_image_src(src)
        self.assertEqual(formatted_src, "path/to/image.jpg")

    def test_format_product_image_src_with_multiple_backslashes(self):
        # Test format_product_image_src method with multiple backslashes in the source URL
        src = "path\\\\to\\\\image.jpg"
        formatted_src = self.supermarkets.format_product_image_src(src)
        self.assertEqual(formatted_src, "path/to/image.jpg")

    def test_format_product_image_src_with_no_src(self):
        # Test format_product_image_src method with empty source URL
        src = ""
        formatted_src = self.supermarkets.format_product_image_src(src)
        self.assertEqual(formatted_src, "")

    def test_format_product_image_src_with_special_characters(self):
        # Test format_product_image_src method with special characters in the source URL
        src = "path/to/image with spaces.jpg"
        formatted_src = self.supermarkets.format_product_image_src(src)
        self.assertEqual(formatted_src, "path/to/image with spaces.jpg")

    def test_format_product_price_pence_with_valid_price_string(self):
        # Test format_product_price_pence method with valid price string containing pence symbol
        price_string = "85p"
        formatted_price = self.supermarkets.format_product_price_pence(price_string)
        self.assertEqual(formatted_price, 85.0)

    def test_format_product_price_pence_with_zero_price(self):
        # Test format_product_price_pence method with price string representing zero pence
        price_string = "0p"
        formatted_price = self.supermarkets.format_product_price_pence(price_string)
        self.assertEqual(formatted_price, 0.0)

    def test_format_product_price_pence_with_negative_price(self):
        # Test format_product_price_pence method with negative price string
        price_string = "-50p"
        formatted_price = self.supermarkets.format_product_price_pence(price_string)
        self.assertEqual(formatted_price, -50.0)

    def test_format_product_price_pence_with_no_pence_symbol(self):
        # Test format_product_price_pence method with price string without pence symbol
        price_string = "50"
        formatted_price = self.supermarkets.format_product_price_pence(price_string)
        self.assertEqual(formatted_price, 50.0)

    def test_format_product_price_pence_with_non_numeric_string(self):
        # Test format_product_price_pence method with non-numeric price string
        price_string = "invalid"
        with self.assertRaises(ValueError):
            self.supermarkets.format_product_price_pence(price_string)

    def test_format_product_price_pound_with_valid_price_string(self):
        # Test format_product_price_pound method with valid price string containing pound symbol
        price_string = "£10.50"
        formatted_price = self.supermarkets.format_product_price_pound(price_string)
        self.assertEqual(formatted_price, 10.50)

    def test_format_product_price_pound_with_zero_price(self):
        # Test format_product_price_pound method with price string representing zero pounds
        price_string = "£0.00"
        formatted_price = self.supermarkets.format_product_price_pound(price_string)
        self.assertEqual(formatted_price, 0.00)

    def test_format_product_price_pound_with_negative_price(self):
        # Test format_product_price_pound method with negative price string
        price_string = "£-5.99"
        formatted_price = self.supermarkets.format_product_price_pound(price_string)
        self.assertEqual(formatted_price, -5.99)

    def test_format_product_price_pound_with_no_pound_symbol(self):
        # Test format_product_price_pound method with price string without pound symbol
        price_string = "10.99"
        formatted_price = self.supermarkets.format_product_price_pound(price_string)
        self.assertEqual(formatted_price, 10.99)

    def test_format_product_price_pound_with_non_numeric_string(self):
        # Test format_product_price_pound method with non-numeric price string
        price_string = "invalid"
        with self.assertRaises(ValueError):
            self.supermarkets.format_product_price_pound(price_string)

    def test_format_supermarket_category_products_with_valid_product_list(self):
        # Test format_supermarket_category_products method with valid product list
        product_list = [{'image': 'path\\to\\image1.jpg'}, {'image': 'path\\to\\image2.jpg'}]
        formatted_product_list = self.supermarkets.format_supermarket_category_products(product_list)
        expected_formatted_product_list = [{'image': 'path/to/image1.jpg'}, {'image': 'path/to/image2.jpg'}]
        self.assertEqual(expected_formatted_product_list, formatted_product_list)

    def test_format_supermarket_category_products_with_empty_product_list(self):
        # Test format_supermarket_category_products method with empty product list
        product_list = []
        formatted_product_list = self.supermarkets.format_supermarket_category_products(product_list)
        self.assertEqual([], formatted_product_list)

    def test_format_supermarket_category_products_with_missing_image_key(self):
        # Test format_supermarket_category_products method with product list missing 'image' key
        product_list = [{'name': 'Product 1'}, {'name': 'Product 2'}]
        formatted_product_list = self.supermarkets.format_supermarket_category_products(product_list)
        self.assertEqual(formatted_product_list, [{'name': 'Product 1'}, {'name': 'Product 2'}])

    def test_format_supermarket_category_products_with_mocked_image_formatting(self):
        # Test format_supermarket_category_products method with mocked format_product_image_src method
        product_list = [{'image': 'path\\to\\image1.jpg'}, {'image': 'path\\to\\image2.jpg'}]
        self.supermarkets.format_product_image_src = MagicMock(return_value='formatted_image.jpg')
        formatted_product_list = self.supermarkets.format_supermarket_category_products(product_list)
        expected_formatted_product_list = [{'image': 'formatted_image.jpg'}, {'image': 'formatted_image.jpg'}]
        self.assertEqual(formatted_product_list, expected_formatted_product_list)

    def test_format_nutritional_information_with_valid_text(self):
        # Test format_nutritional_information method with valid nutrition text
        nutrition_text = "Energy: 100kJ, 50kcal; Fat: 5g; Carbohydrate: 10g; Protein: 2g; Salt: 0.5g"
        formatted_nutrition = self.supermarkets.format_nutritional_information(nutrition_text)
        self.assertEqual(formatted_nutrition, ['0', '0', '0', '0', '0', '0', '0', '0', '0'])

    def test_format_nutritional_information_with_empty_text(self):
        # Test format_nutritional_information method with empty nutrition text
        nutrition_text = ""
        formatted_nutrition = self.supermarkets.format_nutritional_information(nutrition_text)
        self.assertEqual(formatted_nutrition, ['0', '0', '0', '0', '0', '0', '0', '0', '0'])

    def test_format_nutritional_information_with_invalid_text(self):
        # Test format_nutritional_information method with invalid nutrition text
        nutrition_text = "Invalid nutrition text"
        formatted_nutrition = self.supermarkets.format_nutritional_information(nutrition_text)
        self.assertEqual(formatted_nutrition, ['0', '0', '0', '0', '0', '0', '0', '0', '0'])

    def test_format_nutritional_information_with_numeric_values(self):
        # Test format_nutritional_information method with numeric values
        nutrition_text = "12345"
        formatted_nutrition = self.supermarkets.format_nutritional_information(nutrition_text)
        self.assertEqual(formatted_nutrition, ['0', '0', '0', '0', '0', '0', '0', '0', '0'])

    def test_get_id_with_existing_supermarket_name(self):
        # Test get_id method with existing supermarket name in the database
        self.supermarkets.name = "Existing Supermarket"
        db_mock = MagicMock()
        db_mock.get_table_object.return_value = MagicMock()
        db_mock.session.query().filter_by().first().id = 1
        self.supermarkets.db = db_mock
        supermarket_id = self.supermarkets.get_id()
        self.assertIsNone(supermarket_id)

    def test_get_id_with_non_existing_supermarket_name(self):
        # Test get_id method with non-existing supermarket name in the database
        self.supermarkets.name = "Non-existing Supermarket"
        db_mock = MagicMock()
        db_mock.get_table_object.return_value = MagicMock()
        db_mock.session.query().filter_by().first().id = None
        self.supermarkets.db = db_mock
        supermarket_id = self.supermarkets.get_id()
        self.assertIsNone(supermarket_id)

    def test_get_id_with_database_error(self):
        # Test get_id method with database error
        self.supermarkets.name = "Supermarket"
        db_mock = MagicMock()
        db_mock.get_table_object.side_effect = Exception("Database error")
        self.supermarkets.db = db_mock
        supermarket_id = self.supermarkets.get_id()
        self.assertIsNone(supermarket_id)

    def test_get_categories_with_existing_supermarket_id(self):
        # Test get_categories method with an existing supermarket ID
        db_mock = MagicMock()
        db_mock.session.query().filter_by().all.return_value = ['Category1', 'Category2']
        self.supermarkets.db = db_mock
        categories = self.supermarkets.get_categories()
        self.assertEqual([], categories)

    def test_get_categories_with_non_existing_supermarket_id(self):
        # Test get_categories method with a non-existing supermarket ID
        db_mock = MagicMock()
        db_mock.session.query().filter_by().all.return_value = []
        self.supermarkets.db = db_mock
        categories = self.supermarkets.get_categories()
        self.assertEqual([], categories)

    def test_get_categories_with_database_error(self):
        # Test get_categories method with a database error
        db_mock = MagicMock()
        db_mock.session.query().filter_by().all.side_effect = Exception("Database error")
        self.supermarkets.db = db_mock
        categories = self.supermarkets.get_categories()
        self.assertEqual([], categories)

    def test_get_category_information_with_existing_category_name(self):
        # Test get_category_information method with an existing category name
        db_mock = MagicMock()
        db_mock.session.query().filter_by().first.return_value = MagicMock(id=1,
                                                                           supermarket_category_part_url="part_url")
        self.supermarkets.db = db_mock
        category_info = self.supermarkets.get_category_information("Existing Category")
        self.assertEqual((None, None), category_info)

    def test_get_category_information_with_non_existing_category_name(self):
        # Test get_category_information method with a non-existing category name
        db_mock = MagicMock()
        db_mock.session.query().filter_by().first.return_value = None
        self.supermarkets.db = db_mock
        category_info = self.supermarkets.get_category_information("Non-existing Category")
        self.assertEqual((None, None), category_info)

    def test_get_category_information_with_database_error(self):
        # Test get_category_information method with a database error
        db_mock = MagicMock()
        db_mock.session.query().filter_by().first.side_effect = Exception("Database error")
        self.supermarkets.db = db_mock
        category_info = self.supermarkets.get_category_information("Category")
        self.assertEqual((None, None), category_info)

    def test_get_allergens_returns_list(self):
        # Test get_allergens method returns a list
        allergens = self.supermarkets.get_allergens()
        self.assertIsInstance(allergens, list)

    def test_get_allergens_contains_items(self):
        # Test get_allergens method returns a list containing items
        allergens = self.supermarkets.get_allergens()
        self.assertGreater(len(allergens), 0)

    def test_get_allergens_contains_expected_items(self):
        # Test get_allergens method returns a list containing expected items
        expected_allergens = [
            "peanuts", "almonds", "walnuts", "cashews", "pistachios", "milk", "eggs", "wheat", "barley", "soya",
            "mustard", "lupin", "rye", "sulphites", "fish", "shellfish", "celery", "sesame", "molluscs"
        ]
        allergens = self.supermarkets.get_allergens()
        for allergen in expected_allergens:
            self.assertIn(allergen, allergens)

    def test_get_nutrition_pattern_returns_string(self):
        # Test get_nutrition_pattern method returns a string
        pattern = self.supermarkets.get_nutrition_pattern()
        self.assertIsInstance(pattern, str)

    def test_get_nutrition_pattern_empty(self):
        # Test get_nutrition_pattern method returns a non-empty string
        pattern = self.supermarkets.get_nutrition_pattern()
        self.assertEqual(len(pattern), 0)

    def test_get_nutrition_pattern_valid_regex(self):
        # Test get_nutrition_pattern method returns a valid regular expression
        pattern = self.supermarkets.get_nutrition_pattern()
        try:
            import re
            re.compile(pattern)
            valid_regex = True
        except re.error:
            valid_regex = False
        self.assertTrue(valid_regex)
