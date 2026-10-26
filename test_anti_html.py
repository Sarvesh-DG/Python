
import unittest
from unittest.mock import patch, Mock
import requests

from anti_html import anti_html


class TestAntiHtml(unittest.TestCase):

    @patch("anti_html.requests.get")
    def test_removes_html_tags(self, mock_get):
        response = Mock()
        response.text = (
            "<html><body>"
            "<h1>Hello</h1>"
            "<p>World</p>"
            "</body></html>"
        )
        mock_get.return_value = response

        result = anti_html("https://example.com")

        self.assertEqual(result, "Hello\nWorld")
        mock_get.assert_called_once_with(
            "https://example.com", timeout=15
        )
        response.raise_for_status.assert_called_once()

    @patch("anti_html.requests.get")
    def test_empty_html(self, mock_get):
        response = Mock()
        response.text = "<html><body></body></html>"
        mock_get.return_value = response

        result = anti_html("https://example.com")

        self.assertEqual(result, "")

    @patch("anti_html.requests.get")
    def test_request_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError(
            "Connection failed"
        )

        with self.assertRaises(requests.exceptions.ConnectionError):
            anti_html("https://example.com")

    @patch("anti_html.requests.get")
    def test_http_error(self, mock_get):
        response = Mock()
        response.text = "Not Found"
        response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("404 Not Found")
        )
        mock_get.return_value = response

        with self.assertRaises(requests.exceptions.HTTPError):
            anti_html("https://example.com")


if __name__ == "__main__":
    unittest.main()
