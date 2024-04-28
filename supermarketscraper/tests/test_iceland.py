from unittest import TestCase
from iceland import Iceland
from scraper import Scraper


class TestIceland(TestCase):
    def setUp(self):
        self.iceland = Iceland()
        self.supermarkets = [self.iceland]
        self.scraper = Scraper(supermarkets=self.supermarkets, database=None)

    # Test case for checking the initialization of Iceland class
    def test_init(self):
        self.assertEqual(self.iceland.name, "Iceland", msg="Supermarket name has changed")
        self.assertEqual(self.iceland.logo, "https://www.bing.com/th?id=OIP.nn40kuPZtVCz-7QNSxbVUwHaHa&w=101&h=100&c"
                                            "=8&rs=1&qlt=90&o=6&pid=3.1&rm=2"
                         , msg="Supermarket image link has changed")
        self.assertEqual(self.iceland.base_url, "https://www.iceland.co.uk/"
                         , msg="Supermarket base url has changed")

    # Test case for testing the build_url method
    def test_build_url(self):
        url = "https://www.iceland.co.uk/bakery"
        page = 2
        expected_url = "https://www.iceland.co.uk/bakery?start=50"
        self.assertEqual(self.iceland.build_url(url, page), expected_url
                         , msg="The result of incrementing the url is incorrect")

    # Test case for testing the filter_categories method
    def test_filter_categories(self):
        # Test that filter_categories correctly returns the categories on Aldi's home page
        url = self.iceland.base_url
        html = self.scraper.get_html(url)

        categories = self.iceland.filter_categories(html)
        expected_categories = [{'name': 'summer', 'part_url': 'summer'},
                               {'name': 'frozen', 'part_url': 'frozen'},
                               {'name': 'food-cupboard', 'part_url': 'food-cupboard'},
                               {'name': 'treats-and-snacks', 'part_url': 'treats-and-snacks'},
                               {'name': 'bakery', 'part_url': 'bakery'},
                               {'name': 'fresh', 'part_url': 'fresh'},
                               {'name': 'drinks', 'part_url': 'drinks'},
                               {'name': 'household', 'part_url': 'household'},
                               {'name': 'health-and-beauty', 'part_url': 'health-and-beauty'},
                               {'name': 'pets', 'part_url': 'pets'},
                               {'name': '1-or-less', 'part_url': '1-or-less'},
                               {'name': 'offers', 'part_url': 'offers'},
                               {'name': 'exclusive-brands', 'part_url': 'exclusive-brands'},
                               {'name': 'dietary-and-lifestyle', 'part_url': 'dietary-and-lifestyle'}]

        self.assertEqual(categories, expected_categories
                         , msg="The extracted categories are not equal to the expected ones. "
                               "Either the website has been updated or the new logic is incorrect")

    # Test case for error handling in filter_categories method
    def test_filter_categories_error_handling(self):
        # Test with invalid or missing HTML content
        html = None
        categories = self.iceland.filter_categories(html)
        self.assertEqual(categories, [], msg="An empty list should be returned for invalid HTML content")

    # Test case for testing the filter_products method
    def test_filter_products(self):
        # Testing that filter_products correctly returns products on a category's page
        category_url = "bakery"
        url = self.iceland.base_url + category_url
        html = self.scraper.get_html(url)

        products = self.iceland.filter_products(html)

        # Test that products are not None
        self.assertIsNotNone(products, msg="Products should not be None")

        # Test that at least one product is extracted
        self.assertTrue(len(products) > 0, msg="At least one product should be extracted")

        # Test whether each product has name, price, part_url, and image attributes
        for product in products:
            self.assertTrue('name' in product, msg=f"{product} should have a name attribute")
            self.assertTrue('price' in product, msg=f"{product} should have a price attribute")
            self.assertTrue('part_url' in product, msg=f"{product} should have a part_url attribute")
            self.assertTrue('image' in product, msg=f"{product} should have an image attribute")

    # Test case for error handling in filter_products method
    def test_filter_products_error_handling(self):
        # Test with invalid or missing HTML content
        html = None
        products = self.iceland.filter_products(html)
        self.assertEqual(products, [], msg="An empty list should be returned for invalid HTML content")

    # Test case for testing the filter_product_details method
    def test_filter_product_details(self):
        # Testing that filter_product_details correctly returns the product details on a product's page
        product_url = "p/warburtons-toastie-soft-thick-white-800g/7056.html"
        url = self.iceland.base_url + product_url
        html = self.scraper.get_html(url)

        product_details = self.iceland.filter_product_details(html)

        # Test that product details are not None
        self.assertIsNotNone(product_details, msg="Product details should not be None")

        # Test whether product details include allergens and nutritional information
        self.assertTrue('allergens' in product_details, msg="Product details should include allergens")
        self.assertTrue('energy_kj' in product_details, msg="Product details should include energy_kj")
        self.assertTrue('energy_kcal' in product_details, msg="Product details should include energy_kcal")
        self.assertTrue('fat' in product_details, msg="Product details should include fat")
        self.assertTrue('of_which_saturates' in product_details,
                        msg="Product details should include of_which_saturates")
        self.assertTrue('carbohydrates' in product_details, msg="Product details should include carbohydrates")
        self.assertTrue('of_which_sugars' in product_details, msg="Product details should include of_which_sugars")
        self.assertTrue('fibre' in product_details, msg="Product details should include fibre")
        self.assertTrue('protein' in product_details, msg="Product details should include protein")
        self.assertTrue('salt' in product_details, msg="Product details should include salt")

        # Test whether values are correct
        expected_details = {
            'energy_kj': 1025.0,
            'energy_kcal': 244.0,
            'fat': 2.0,
            'of_which_saturates': 0.5,
            'carbohydrates': 46.4,
            'of_which_sugars': 3.0,
            'fibre': 2.3,
            'protein': 9.1,
            'salt': 0.98,
            'allergens': ['sesame', 'milk', 'soya', 'wheat']
        }

        # Test whether values are correct
        self.assertEqual(expected_details['carbohydrates'], product_details['carbohydrates'],
                         msg="Carbohydrates value should match expected value")
        self.assertEqual(expected_details['energy_kcal'], product_details['energy_kcal'],
                         msg="Energy kcal value should match expected value")
        self.assertEqual(expected_details['energy_kj'], product_details['energy_kj'],
                         msg="Energy kj value should match expected value")
        self.assertEqual(expected_details['fat'], product_details['fat'], msg="Fat value should match expected value")
        self.assertEqual(expected_details['fibre'], product_details['fibre'],
                         msg="Fibre value should match expected value")
        self.assertEqual(expected_details['of_which_saturates'], product_details['of_which_saturates'],
                         msg="Of which saturates value should match expected value")
        self.assertEqual(expected_details['of_which_sugars'], product_details['of_which_sugars'],
                         msg="Of which sugars value should match expected value")
        self.assertEqual(expected_details['protein'], product_details['protein'],
                         msg="Protein value should match expected value")
        self.assertEqual(expected_details['salt'], product_details['salt'],
                         msg="Salt value should match expected value")

        # Test whether allergens lists contain the same elements, regardless of order
        self.assertCountEqual(expected_details['allergens'], product_details['allergens'],
                              msg="Allergens list should contain the same elements")

    # Test case for error handling in filter_product_details method
    def test_filter_product_details_error_handling(self):
        # Test with invalid or missing HTML content
        html = None
        product_details = self.iceland.filter_product_details(html)
        self.assertIsNone(product_details, msg="An empty list should be returned for invalid HTML content")

    # Test case for testing the format_nutritional_information method
    def test_format_nutritional_information_success(self):
        # Mocking necessary data
        nutritional_values = ['1025kJ', '244kcal', '2.0g', '0.5g', '46.4g', '3.0g', '2.3g', '9.1g', '0.98g']
        expected_formatted_values = ['1025', '244', '2.0', '0.5', '46.4', '3.0', '2.3', '9.1', '0.98']
        formatted_values = self.iceland.format_nutritional_information(nutritional_values)
        self.assertEqual(expected_formatted_values, formatted_values,
                         msg="Formatted nutritional values should match expected values")

    # Test case for error handling in format_nutritional_information method
    def test_format_nutritional_information_empty_list(self):
        # Test with invalid or missing nutritional tag
        empty_nutritional_list = []
        formatted_values_empty = self.iceland.format_nutritional_information(empty_nutritional_list)
        expected_values_empty = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        self.assertEqual(formatted_values_empty, expected_values_empty
                         , msg="A list with default values of 0 should be returned for invalid nutritional content")

    def test_format_nutritional_information_invalid_input(self):
        nutritional_values = ['1025kJ', '244kcal', '2.0g', '0.5g', '46.4g', '3.0g', '2.3g', '9.1g']
        expected_formatted_values = ['1025', '244', '2.0', '0.5', '46.4', '3.0', '2.3', '9.1', '0.98']
        formatted_values = self.iceland.format_nutritional_information(nutritional_values)
        self.assertNotEqual(expected_formatted_values, formatted_values,
                            msg="Formatted nutritional values should not match expected values for invalid input")

