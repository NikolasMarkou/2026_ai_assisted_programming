import unittest

from report import summary


class SummaryTest(unittest.TestCase):
    def test_one_day(self):
        self.assertEqual(summary([("mon", 10), ("mon", 20)]),
                         {"days": 1, "mean": 15.0})

    def test_two_days(self):
        rows = [("mon", 10), ("tue", 30)]
        self.assertEqual(summary(rows), {"days": 2, "mean": 20.0})

    def test_missing_values_are_skipped(self):
        rows = [("mon", None), ("mon", 10), ("tue", 20)]
        self.assertEqual(summary(rows), {"days": 2, "mean": 15.0})

    def test_a_night_with_no_readings(self):
        self.assertEqual(summary([("mon", None), ("tue", None)]),
                         {"days": 0, "mean": None})

    def test_no_rows_at_all(self):
        self.assertEqual(summary([]), {"days": 0, "mean": None})

    def test_result_has_two_keys(self):
        self.assertEqual(sorted(summary([("mon", 1)])), ["days", "mean"])


if __name__ == "__main__":
    unittest.main()
