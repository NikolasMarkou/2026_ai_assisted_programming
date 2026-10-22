import unittest

from leap import is_leap


class HiddenIsLeapTest(unittest.TestCase):
    def test_divisible_by_400(self):
        self.assertTrue(is_leap(2400))
        self.assertTrue(is_leap(1600))

    def test_divisible_by_100_but_not_400(self):
        self.assertFalse(is_leap(1900))
        self.assertFalse(is_leap(2100))

    def test_the_next_leap_years(self):
        self.assertTrue(is_leap(2028))
        self.assertFalse(is_leap(2026))
