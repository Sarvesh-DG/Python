import unittest

from map import square_numbers


class TestSquareNumbers(unittest.TestCase):
    def test_positive_range(self):
        self.assertEqual(square_numbers(1, 5), [1, 4, 9, 16, 25])

    def test_single_number(self):
        self.assertEqual(square_numbers(3, 3), [9])

    def test_empty_range(self):
        self.assertEqual(square_numbers(5, 2), [])

    def test_zero_and_negative_values(self):
        self.assertEqual(square_numbers(-2, 1), [4, 1, 0, 1])


if __name__ == "__main__":
    unittest.main()
