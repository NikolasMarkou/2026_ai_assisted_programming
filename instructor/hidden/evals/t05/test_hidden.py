import unittest

from ratio import percent


class HiddenPercentTest(unittest.TestCase):
    def test_rounds_to_one_decimal(self):
        self.assertEqual(percent(1, 3), 33.3)

    def test_zero_total_with_a_part(self):
        self.assertEqual(percent(5, 0), 0.0)

    def test_whole(self):
        self.assertEqual(percent(8, 8), 100.0)

    def test_zero_part(self):
        self.assertEqual(percent(0, 9), 0.0)
