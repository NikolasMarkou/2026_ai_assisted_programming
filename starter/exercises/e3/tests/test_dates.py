import unittest
from datetime import datetime, timezone

from src.dates import parse_date


def utc(*args):
    return datetime(*args, tzinfo=timezone.utc)


class ParseDateTest(unittest.TestCase):
    def test_positive_offset(self):
        self.assertEqual(parse_date("2026-10-22T09:00+02:00"), utc(2026, 10, 22, 7))

    def test_negative_offset(self):
        self.assertEqual(parse_date("2026-10-22T09:00-05:00"), utc(2026, 10, 22, 14))

    def test_offset_that_crosses_midnight(self):
        self.assertEqual(parse_date("2026-10-22T01:00+03:00"), utc(2026, 10, 21, 22))

    def test_half_hour_offset(self):
        self.assertEqual(parse_date("2026-10-22T12:00+05:30"), utc(2026, 10, 22, 6, 30))

    def test_offset_that_crosses_the_year_end(self):
        self.assertEqual(parse_date("2026-12-31T23:30-02:00"), utc(2027, 1, 1, 1, 30))


if __name__ == "__main__":
    unittest.main()
