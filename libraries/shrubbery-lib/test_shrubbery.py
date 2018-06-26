import unittest
import shrubberylib


class ShrubberyTestCase(unittest.TestCase):
    def test_shrubbery(self):
        x = shrubberylib.Shrubbery(5, 10)
        area = x.get_area()
        perimeter = x.get_perimeter()
        self.assertEqual(area, 50)
        self.assertEqual(perimeter, 30)
