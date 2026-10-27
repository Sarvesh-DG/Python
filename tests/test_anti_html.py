import unittest
from unittest.mock import Mock, patch

import requests

from anti_html import anti_html


class TestAntiHtml(unittest.TestCase):
    @patch("anti_html.requests.get")
    def test_extracts_text_and_uses_timeout(self, mock_get):
        response = Mock(text="<h1>Hello</h1><p>World</p>")
        mock_get.return_value = response
        self.assertEqual(anti_html("https://example.com"), "Hello\nWorld")
        mock_get.assert_called_once_with("https://example.com", timeout=15)
        response.raise_for_status.assert_called_once()

    @patch("anti_html.requests.get")
    def test_empty_document(self, mock_get):
        mock_get.return_value = Mock(text="<html><body></body></html>")
        self.assertEqual(anti_html("https://example.com"), "")

    def test_rejects_invalid_url_before_network(self):
        with patch("anti_html.requests.get") as mock_get:
            with self.assertRaises(ValueError):
                anti_html("example.com")
            mock_get.assert_not_called()

    @patch("anti_html.requests.get", side_effect=requests.ConnectionError("offline"))
    def test_connection_failure_propagates(self, _mock_get):
        with self.assertRaises(requests.ConnectionError):
            anti_html("https://example.com")

    @patch("anti_html.requests.get")
    def test_http_error_propagates(self, mock_get):
        response = Mock(text="nope")
        response.raise_for_status.side_effect = requests.HTTPError("404")
        mock_get.return_value = response
        with self.assertRaises(requests.HTTPError):
            anti_html("https://example.com")


if __name__ == "__main__":
    unittest.main()
