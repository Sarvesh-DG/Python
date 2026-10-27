import unittest
from abc import ABC

from abc1 import Female, Male, Person


class TestPersonImplementations(unittest.TestCase):
    def test_male_label(self):
        self.assertEqual(Male().get_gender(), "Male")

    def test_female_label(self):
        self.assertEqual(Female().get_gender(), "Female")

    def test_abstract_base_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Person()

    def test_incomplete_subclass_cannot_be_instantiated(self):
        class IncompletePerson(Person):
            pass

        with self.assertRaises(TypeError):
            IncompletePerson()


if __name__ == "__main__":
    unittest.main()
