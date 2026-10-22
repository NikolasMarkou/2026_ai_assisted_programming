"""Hidden tests for E9. Run from this folder, with the pair's folder on PYTHONPATH:
PYTHONPATH=<the pair's exercises/e9 folder> python3 -B -m unittest -q test_hidden
Never copy this file into the pair's folder.
"""
import unittest

from report import summary


class HiddenReportTest(unittest.TestCase):
    def test_all_values_missing_gives_an_empty_report(self):
        rows = [("mon", None), ("tue", None), ("tue", None)]
        self.assertEqual(summary(rows), {"days": 0, "mean": None})

    def test_no_rows_gives_an_empty_report(self):
        self.assertEqual(summary([]), {"days": 0, "mean": None})

    def test_one_missing_day_does_not_count_as_a_day(self):
        rows = [("mon", None), ("tue", 8), ("tue", 12)]
        self.assertEqual(summary(rows), {"days": 1, "mean": 10.0})

    def test_mean_is_the_mean_of_daily_means(self):
        rows = [("mon", 1), ("mon", 1), ("mon", 4), ("tue", 10)]
        self.assertEqual(summary(rows), {"days": 2, "mean": 6.0})

    def test_zero_is_a_value_not_a_missing_reading(self):
        self.assertEqual(summary([("mon", 0)]), {"days": 1, "mean": 0.0})


if __name__ == "__main__":
    unittest.main()
