from unittest import TestCase
from unittest.mock import patch, Mock
from scraper import Scraper

from aldi import Aldi
from morrisons import Morrisons


class TestScraper(TestCase):

    @patch('scraper.Scraper.get_html', return_value='<html><body><p>Test HTML</p></body></html>')
    def test_scrape(self, mock_get_html):
        # Create mock supermarkets
        mock_1 = Aldi()
        mock_2 = Morrisons()
        mock_supermarkets = [mock_1, mock_2]
        # Mock database
        mock_database = Mock()
        scraper = Scraper(mock_supermarkets, mock_database)

        # Call the method under test
        scraper.scrape()

        # Check if get_html method is called twice (once for each supermarket)
        self.assertEqual(mock_get_html.call_count, 2)

    @patch('scraper.Scraper.get_html', return_value='<html><body><p>Test HTML</p></body></html>')
    def test_scrape_cycle(self, mock_get_html):
        mock_supermarket = Aldi()
        mock_supermarkets = [mock_supermarket]
        mock_database = Mock()

        scraper = Scraper(mock_supermarkets, mock_database)

        scraper.scrape_cycle()

        # Check if get_html method is called once
        self.assertEqual(mock_get_html.call_count, 1)

    def test_get_html(self):
        # Test when URL is valid
        valid_url = 'https://groceries.aldi.co.uk/en-GB/bakery?'
        scraper = Scraper([], None)
        html = scraper.get_html(valid_url)
        self.assertIsNotNone(html)

        # Test when URL is invalid
        invalid_url = 'https://'
        html = scraper.get_html(invalid_url)
        self.assertIsNone(html)

    @patch('scraper.Scraper.get_page', return_value='<html><body><p>Test HTML</p></body></html>')
    def test_get_page(self, mock_get_page):
        valid_url = 'https://groceries.aldi.co.uk/en-GB/bakery?&page=2'
        scraper = Scraper([], None)
        html = scraper.get_html(valid_url)
        self.assertIsNotNone(html)

