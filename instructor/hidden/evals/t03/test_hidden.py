import unittest

from stats import median


class HiddenMedianTest(unittest.TestCase):
    def test_two_values(self):
        self.assertEqual(median([10, 20]), 15)

    def test_even_count_unsorted(self):
        self.assertEqual(median([9, 1, 5, 7, 3, 11]), 6)

    def test_one_value(self):
        self.assertEqual(median([7]), 7)

    def test_empty_is_rejected(self):
        with self.assertRaises(ValueError):
            median([])
