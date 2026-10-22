import unittest

from ratio import percent


class PercentTest(unittest.TestCase):
    def test_quarter(self):
        self.assertEqual(percent(1, 4), 25.0)

    def test_empty_report(self):
        self.assertEqual(percent(0, 0), 0.0)
