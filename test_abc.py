from abc1 import Person,Male,Female
import unittest
class TestABC(unittest.TestCase):
    def test_abc_male(self):
        male=Male()
        self.assertEqual(male.get_gender(),"Male")
    def test_abc_female(self):
            female=Female()
            self.assertEqual(female.get_gender(),"Female")


