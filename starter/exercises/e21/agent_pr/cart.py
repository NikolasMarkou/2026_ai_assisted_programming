"""Cart totals in whole cents, with a cap on the discount.

Usage: python3 cart.py [--discount PERCENT] PRICE_CENTS [PRICE_CENTS ...]
Prints the discount asked for, the discount applied and the total. The tests are at
the bottom of this file.
"""
import argparse
import unittest

MAX_DISCOUNT = 50


def clamp_discount(percent):
    """The discount limited to the range 0 to MAX_DISCOUNT."""
    return max(0, min(percent, MAX_DISCOUNT))


def total_cents(prices_cents, discount=0):
    """Sum of the prices after a percent discount, in whole cents (rounded half up)."""
    left = 100 - clamp_discount(discount)
    return (sum(prices_cents) * left * 2 + 100) // 200


def dollars(cents):
    """Whole cents as text, 1250 becomes 12.50."""
    return f"{cents // 100}.{cents % 100:02d}"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Total of a cart in cents.")
    parser.add_argument("--discount", type=int, default=0)
    parser.add_argument("prices", type=int, nargs="+")
    args = parser.parse_args(argv)
    applied = clamp_discount(args.discount)
    print(f"discount asked: {args.discount} percent, applied: {applied} percent")
    print(f"total: {dollars(total_cents(args.prices, args.discount))}")
    return 0


class TestTotal(unittest.TestCase):
    def test_no_discount(self):
        self.assertEqual(total_cents([1000, 250]), 1250)

    def test_ten_percent(self):
        self.assertEqual(total_cents([1000, 250], 10), 1125)

    def test_rounds_half_up(self):
        self.assertEqual(total_cents([285], 50), 143)


if __name__ == "__main__":
    raise SystemExit(main())
