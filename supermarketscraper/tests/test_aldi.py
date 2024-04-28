from unittest import TestCase
from aldi import Aldi
from scraper import Scraper


class TestAldi(TestCase):
    def setUp(self):
        self.aldi = Aldi()
        self.supermarkets = [self.aldi]
        self.scraper = Scraper(supermarkets=self.supermarkets, database=None)

    # Test case for checking the initialising of Aldi class
    def test_init(self):
        self.assertEqual(self.aldi.name, "Aldi", msg="Supermarket name has changed")
        self.assertEqual(self.aldi.logo, "https://cdn.aldi-digital.co.uk/32FDVWu4Lhbxgj9Z3v03ji0pGJIp?&w=70&h=84"
                         , msg="Supermarket image link has changed")
        self.assertEqual(self.aldi.base_url, "https://groceries.aldi.co.uk"
                         , msg="Supermarket base url has changed")

    # Test case for testing the build_url method
    def test_build_url(self):
        url = "https://groceries.aldi.co.uk"
        page = 1
        expected_url = "https://groceries.aldi.co.uk&page=1"
        self.assertEqual(self.aldi.build_url(url, page), expected_url
                         , msg="The result of incrementing the url is incorrect")

    # Test case for testing the filter_categories method
    def test_filter_categories(self):
        # Test that filter_categories correctly returns the categories on Aldi's home page
        url = self.aldi.base_url
        html = self.scraper.get_html(url)

        categories = self.aldi.filter_categories(html)
        expected_categories = [{'name': 'specially selected', 'part_url': '/en-GB/specially-selected?'},
                               {'name': 'vegan & plant based', 'part_url': '/en-GB/vegan-range?'},
                               {'name': 'bakery', 'part_url': '/en-GB/bakery?'},
                               {'name': 'fresh food', 'part_url': '/en-GB/fresh-food?'},
                               {'name': 'drinks', 'part_url': '/en-GB/drinks?'},
                               {'name': 'food cupboard', 'part_url': '/en-GB/food-cupboard?'},
                               {'name': 'frozen food', 'part_url': '/en-GB/frozen?'},
                               {'name': 'chilled food', 'part_url': '/en-GB/chilled-food?'},
                               {'name': 'baby & toddler', 'part_url': '/en-GB/baby-toddler?'},
                               {'name': 'health & beauty', 'part_url': '/en-GB/health-beauty?'},
                               {'name': 'household', 'part_url': '/en-GB/household?'},
                               {'name': 'pet care', 'part_url': '/en-GB/pet-care?'},
                               {'name': 'beers & ciders', 'part_url': '/en-GB/drinks/beers-ciders?'},
                               {'name': 'wines', 'part_url': '/en-GB/drinks/wine?'},
                               {'name': 'spirits & liqueurs', 'part_url': '/en-GB/drinks/spirits-liqueurs?'},
                               {'name': 'healthy meals', 'part_url': '/en-GB/healthy-meals?'},
                               {'name': 'lunch box', 'part_url': '/en-GB/lunch-box?'},
                               {'name': 'big night in', 'part_url': '/en-GB/big-night-in?'},
                               {'name': 'vegan range', 'part_url': '/en-GB/vegan-range?'},
                               {'name': 'roast dinner', 'part_url': '/en-GB/roast-dinner?'},
                               {'name': 'afternoon tea', 'part_url': '/en-GB/afternoon-tea?'}]

        self.assertEqual(categories, expected_categories
                         , msg="The extracted categories are not equal to the expected ones. "
                               "Either the website has been updated or the new logic is incorrect")

    # Test case for error handling in filter_categories method
    def test_filter_categories_error_handling(self):
        # Test with invalid or missing HTML content
        html = None
        categories = self.aldi.filter_categories(html)
        self.assertEqual(categories, [], msg="An empty list should be returned for invalid HTML content")

    # Test case for testing the filter_products method
    def test_filter_products(self):
        # Testing that filter_products correctly returns products on a category's page
        category_url = "/en-GB/bakery?"
        url = self.aldi.base_url + category_url
        html = self.scraper.get_html(url)

        products = self.aldi.filter_products(html)

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
        products = self.aldi.filter_products(html)
        self.assertEqual(products, [], msg="An empty list should be returned for invalid HTML content")

    # Test case for testing the filter_product_details method
    def test_filter_product_details(self):
        # Testing that filter_product_details correctly returns the product details on a product's page
        product_url = "/en-GB/p-village-bakery-toastie-thick-sliced-white-bread-800g/4088600253305"
        url = self.aldi.base_url + product_url
        html = self.scraper.get_html(url)

        product_details = self.aldi.filter_product_details(html)

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
            'energy_kj': 1009.0,
            'energy_kcal': 239.0,
            'fat': 2.0,
            'of_which_saturates': 0.5,
            'carbohydrates': 45.0,
            'of_which_sugars': 2.9,
            'fibre': 3.6,
            'protein': 8.3,
            'salt': 0.87,
            'allergens': ['wheat', 'soya'],
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
        product_details = self.aldi.filter_product_details(html)
        self.assertIsNone(product_details, msg="An empty list should be returned for invalid HTML content")

    # Test case for testing the format_nutritional_information method
    def test_format_nutritional_information(self):
        # Mocking necessary data
        nutrition_text_1 = ("Per 100g:Energy 1009kJ, 239kcalFat 2.0gof which saturates 0.5gCarbohydrate 45gof which "
                            "sugars 2.9gFibre 3.6gProtein 8.3gSalt 0.87g")
        expected_values_1 = ['1009', '239', '2.0', '0.5', '45', '2.9', '3.6', '8.3', '0.87']

        nutrition_text_2 = "Per 100g:Energy 1423kJ, 435kcal"
        expected_values_2 = ['1423', '435', '0', '0', '0', '0', '0', '0', '0']

        # Call the method under test
        formatted_values_1 = self.aldi.format_nutritional_information(nutrition_text_1)
        formatted_values_2 = self.aldi.format_nutritional_information(nutrition_text_2)

        # Assert the output matches the expected values
        self.assertEqual(expected_values_1, formatted_values_1
                         , msg="The formatted nutritional information does not match the expected values")
        self.assertEqual(expected_values_2, formatted_values_2, msg="The formatted nutritional information does not "
                                                                    "maths the expected values")

    # Test case for error handling in format_nutritional_information method
    def test_format_nutritional_information_error_handling(self):
        # Test with invalid or missing nutritional tag
        empty_nutritional_tag = ""
        formatted_values_empty = self.aldi.format_nutritional_information(empty_nutritional_tag)
        expected_values_empty = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        self.assertEqual(formatted_values_empty, expected_values_empty
                         , msg="A list with default values of 0 should be returned for invalid nutritional content")
