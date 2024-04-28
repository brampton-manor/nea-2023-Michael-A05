from unittest import TestCase
from morrisons import Morrisons
from scraper import Scraper
from bs4 import BeautifulSoup


class TestMorrisons(TestCase):
    def setUp(self):
        self.morrisons = Morrisons()
        self.supermarkets = [self.morrisons]
        self.scraper = Scraper(supermarkets=self.supermarkets, database=None)

    # Test case for checking the initialising of Morrisons class
    def test_init(self):
        self.assertEqual(self.morrisons.name, "Morrisons", msg="Supermarket name has changed")
        self.assertEqual(self.morrisons.logo, "https://groceries.morrisons.com/static/morrisonslogo-fe24a.svg"
                         , msg="Supermarket image link has changed")
        self.assertEqual(self.morrisons.base_url, "https://groceries.morrisons.com/browse"
                         , msg="Supermarket base url has changed")

    # Test case for testing the build_url method with different input
    def test_build_url_placeholder(self):
        self.assertEqual(self.morrisons.build_url("", 1), "")

        url_1 = "https://groceries.morrisons.com/browse"
        url_2 = "https://groceries.morrisons.com/browse/category"
        page_number_1 = 1
        page_number_2 = 2

        # Test build_url method with different inputs
        self.assertEqual(self.morrisons.build_url(url_1, page_number_1), "")
        self.assertEqual(self.morrisons.build_url(url_2, page_number_2), "")

    # Test case for testing the filter_categories method
    def test_filter_categories(self):
        # Test that filter_categories correctly returns the categories on Morrison's home page
        url = self.morrisons.base_url
        html = self.scraper.get_html(url)

        categories = self.morrisons.filter_categories(html)
        expected_categories = [{'name': 'More Card Points ', 'part_url': '/more-card-points-188711'},
                               {'name': 'New Homeware Range ', 'part_url': '/new-homeware-range-190076'},
                               {'name': 'Meat & Poultry', 'part_url': '/meat-poultry-179549'},
                               {'name': 'Fish & Seafood', 'part_url': '/fish-seafood-184367'},
                               {'name': 'Fruit & Veg', 'part_url': '/fruit-veg-176738'},
                               {'name': 'Fresh', 'part_url': '/fresh-176739'},
                               {'name': 'Bakery & Cakes', 'part_url': '/bakery-cakes-102210'},
                               {'name': 'Food Cupboard', 'part_url': '/food-cupboard-102705'},
                               {'name': 'Chocolate & Sweets', 'part_url': '/chocolate-sweets-106130'},
                               {'name': 'Frozen', 'part_url': '/frozen-180331'},
                               {'name': 'Drinks', 'part_url': '/drinks-103644'},
                               {'name': 'Beer, Wines & Spirits', 'part_url': '/beer-wines-spirits-103120'},
                               {'name': 'Toiletries & Beauty', 'part_url': '/toiletries-beauty-102838'},
                               {'name': 'Household', 'part_url': '/household-102063'},
                               {'name': 'Home & Garden', 'part_url': '/home-garden-166274'},
                               {'name': 'Health, Wellbeing & Medicines',
                                'part_url': '/health-wellbeing-medicines-103497'},
                               {'name': 'Baby & Toddler', 'part_url': '/baby-toddler-177598'},
                               {'name': 'Toys & Entertainment', 'part_url': '/toys-entertainment-166275'},
                               {'name': 'Pet Shop', 'part_url': '/pet-shop-102207'},
                               {'name': 'Free From', 'part_url': '/free-from-175652'},
                               {'name': 'World Foods', 'part_url': '/world-foods-182137'}]

        self.assertEqual(expected_categories, categories
                         , msg="The extracted categories are not equal to the expected ones. "
                               "Either the website has been updated or the new logic is incorrect")

    # Test case for error handling in filter_categories method
    def test_filter_categories_error_handling(self):
        # Test with invalid or missing HTML content
        html = None
        categories = self.morrisons.filter_categories(html)
        self.assertEqual(categories, [], msg="An empty list should be returned for invalid HTML content")

    # Test case for testing the filter_products method
    def test_filter_products(self):
        # Testing that filter_products correctly returns products on a category's page
        category_url = "/bakery-cakes-102210"
        url = self.morrisons.base_url + category_url
        html = self.scraper.get_html(url)

        products = self.morrisons.filter_products(html)

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
        products = self.morrisons.filter_products(html)
        self.assertEqual(products, [], msg="An empty list should be returned for invalid HTML content")

    # Test case for the filter_product_details method
    def test_filter_product_details(self):
        # Testing that filter_product_details correctly returns the product details on a product's page
        product_url = "/products/roberts-thick-soft-white-bread-280751011"
        url = self.morrisons.base_url.replace("/browse", "") + product_url
        html = self.scraper.get_html(url)

        product_details = self.morrisons.filter_product_details(html)

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
            'energy_kj': 974.0,
            'energy_kcal': 230.0,
            'fat': 1.0,
            'of_which_saturates': 0.3,
            'carbohydrates': 45.1,
            'of_which_sugars': 4.0,
            'fibre': 3.4,
            'protein': 8.5,
            'salt': 1.0,
            'allergens': ['soya', 'wheat'],
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
        product_details = self.morrisons.filter_product_details(html)
        self.assertIsNone(product_details, msg="An empty list should be returned for invalid HTML content")

    # Test case for the format_nutritional_information method
    def test_format_nutritional_information(self):
        # Example HTML content for nutritional information
        nutritional_tag_content = ("<tbody><tr><th>Typical Values</th><th>Per 100g</th><th>Per "
                                   "Serving</th><th>RI*</th></tr><tr><td>Energy</td><td>974kJ</td><td>468kJ</td><td"
                                   ">8400kJ</td></tr><tr><td></td><td>230kcal</td><td>110kcal</td><td>2000kcal</td"
                                   "></tr><tr><td>Fat</td><td>1.0g</td><td>0.5g</td><td>70g</td></tr><tr><td>of which "
                                   "saturates</td><td>0.3g</td><td>0.1g</td><td>20g</td></tr><tr><td>Carbohydrates"
                                   "</td><td>45.1g</td><td>21.6g</td><td>260g</td></tr><tr><td>of which "
                                   "sugars</td><td>4.0g</td><td>1.9g</td><td>90g</td></tr><tr><td>Fibre</td><td>3.4g"
                                   "</td><td>1.6g</td><td>24g</td></tr><tr><td>Protein</td><td>8.5g</td><td>4.1g</td"
                                   "><td>50g</td></tr><tr><td>Salt</td><td>1.0g</td><td>0.5g</td><td>6g</td></tr><tr"
                                   "><td>* RI - Reference intake of an average "
                                   "adult</td><td></td><td></td><td></td></tr></tbody>")

        # Test if the formatted values are correct
        nutritional_tag = BeautifulSoup(nutritional_tag_content, "html.parser").tbody
        formatted_values = self.morrisons.format_nutritional_information(nutritional_tag)
        expected_values = ['974', '230', '1.0', '0.3', '45.1', '4.0', '3.4', '8.5', '1.0']
        self.assertEqual(formatted_values, expected_values, msg="The formatted nutritional information "
                                                                "does not match the expected values")

    # Test case for error handling in format_nutritional_information method
    def test_format_nutritional_information_error_handling(self):
        # Test with invalid or missing nutritional tag
        empty_nutritional_tag = BeautifulSoup("", 'html.parser').tbody
        formatted_values_empty = self.morrisons.format_nutritional_information(empty_nutritional_tag)
        expected_values_empty = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        self.assertEqual(formatted_values_empty, expected_values_empty, msg="A list with default values of 0 should "
                                                                            "be returned for invalid nutritional "
                                                                            "content")
