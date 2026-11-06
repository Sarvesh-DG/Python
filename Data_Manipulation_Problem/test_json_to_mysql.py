import unittest
import pandas as pd
from json_to_mysql import (
    clean_postal_zip, encode_phone, normalize_email, transform_data
)


class DataManipulationTests(unittest.TestCase):
    def test_email_normalization(self):
        self.assertEqual(normalize_email(" Alice.Test@yahoo.com "), "Alice.Test@gmail.com")

    def test_email_invalid(self):
        with self.assertRaises(ValueError):
            normalize_email("not-an-email")

    def test_postal_code_digits_only(self):
        self.assertEqual(clean_postal_zip("M5V-3A8"), "538")

    def test_postal_code_preserves_leading_zero(self):
        self.assertEqual(clean_postal_zip("00123"), "00123")

    def test_phone_values_below_65_become_letter_o(self):
        self.assertEqual(encode_phone("01-64"), "OO")

    def test_phone_pairs_convert_to_ascii(self):
        self.assertEqual(encode_phone("65-66"), "AB")

    def test_odd_digit_count_ignores_final_digit(self):
        self.assertEqual(encode_phone("65667"), "AB")

    def test_eleven_digit_country_code_is_removed(self):
        self.assertEqual(encode_phone("1-6566-677777"), "ABCMM")

    def test_eleven_digit_without_country_code_ignores_last_digit(self):
        self.assertEqual(encode_phone("65666777777"), "ABCMM")

    def test_transform_does_not_mutate_original(self):
        original = pd.DataFrame({
            "email": ["a@yahoo.com"],
            "postalZip": ["00123"],
            "phone": ["65667"],
        })
        result = transform_data(original)
        self.assertIn("coded_phone_number", result.columns)
        self.assertIn("phone", original.columns)
        self.assertEqual(result.loc[0, "coded_phone_number"], "AB")


if __name__ == "__main__":
    unittest.main()
