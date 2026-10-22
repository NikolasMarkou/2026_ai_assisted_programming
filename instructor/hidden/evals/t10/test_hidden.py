import unittest

from roman import to_roman


class HiddenToRomanTest(unittest.TestCase):
    def test_nine_and_fourteen(self):
        self.assertEqual(to_roman(9), "IX")
        self.assertEqual(to_roman(14), "XIV")

    def test_tens_and_hundreds(self):
        self.assertEqual(to_roman(40), "XL")
        self.assertEqual(to_roman(90), "XC")
        self.assertEqual(to_roman(400), "CD")
        self.assertEqual(to_roman(900), "CM")

    def test_a_long_one(self):
        self.assertEqual(to_roman(1994), "MCMXCIV")
        self.assertEqual(to_roman(3999), "MMMCMXCIX")

    def test_out_of_range_is_rejected(self):
        for number in (0, 4000):
            with self.assertRaises(ValueError):
                to_roman(number)
