from remove_duplicates import remove_duplicates
import unittest

class TestRemoveDuplicates(unittest.TestCase):
    def test_remove_duplicate(self):
        self.assertEqual(remove_duplicates([12,24,35,24,88,120,155,88,120,155]),[12,24,35,88,120,155])