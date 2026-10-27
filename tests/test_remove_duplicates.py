import unittest

from remove_duplicates import remove_duplicates


class TestRemoveDuplicates(unittest.TestCase):
    def test_preserves_first_occurrence_order(self):
        self.assertEqual(
            remove_duplicates([12, 24, 35, 24, 88, 120, 155, 88, 120, 155]),
            [12, 24, 35, 88, 120, 155],
        )

    def test_empty_input(self):
        self.assertEqual(remove_duplicates([]), [])

    def test_no_duplicates(self):
        self.assertEqual(remove_duplicates([1, 2, 3]), [1, 2, 3])

    def test_unhashable_values_raise_clear_native_error(self):
        with self.assertRaises(TypeError):
            remove_duplicates([[1], [1]])


if __name__ == "__main__":
    unittest.main()
