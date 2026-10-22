import unittest

from roman import to_roman


class ToRomanTest(unittest.TestCase):
    def test_additive_numerals(self):
        self.assertEqual(to_roman(3), "III")
        self.assertEqual(to_roman(8), "VIII")

    def test_four(self):
        self.assertEqual(to_roman(4), "IV")
