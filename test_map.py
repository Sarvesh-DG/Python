from map import sqaure_numbers
import unittest

class TestMap(unittest.TestCase):
    def test_map(self):
        self.assertEqual(sqaure_numbers(1,5),[1,4,9,16,25])