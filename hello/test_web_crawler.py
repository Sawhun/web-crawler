import unittest
from unittest.mock import patch, Mock
import requests
from bs4 import BeautifulSoup
from web import WebCrawlerApp


class TestWebCrawler(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_links_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><a href="http://example.com">Example</a></body></html>'
        mock_get.return_value = mock_response



    @patch('requests.get')
    def test_fetch_links_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Error")


if __name__ == "__main__":
    unittest.main()