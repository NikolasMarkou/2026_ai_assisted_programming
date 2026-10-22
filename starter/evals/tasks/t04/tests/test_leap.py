import unittest

from leap import is_leap


class IsLeapTest(unittest.TestCase):
    def test_ordinary_leap_year(self):
        self.assertTrue(is_leap(2024))

    def test_ordinary_year(self):
        self.assertFalse(is_leap(2023))

    def test_year_2000(self):
        self.assertTrue(is_leap(2000))
