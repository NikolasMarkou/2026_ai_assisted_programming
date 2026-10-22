"""Characterization tests: they pin what legacy.py does today, right or wrong.

Every expected value below was produced by running the code before any change.
A failing test after a refactor means the behaviour changed.
"""
import unittest

from legacy import check_country, load_coupons, process_orders, quote_shipping, summary


def make(oid, country, items, **extra):
    return {"id": oid, "country": country, "items": items, **extra}


SHIPPING = [  # country, subtotal in cents, express, fee in cents
    ("DE", 0, False, 499), ("DE", 4999, False, 499), ("DE", 5000, False, 0),
    ("CY", 100, True, 1498), ("FR", 100, False, 1199), ("FR", 5000, True, 1699),
    ("US", 4999, True, 2198), ("XX", 9000, False, 700),
]
COUNTRIES = [("DE", 19), ("FR", 20), ("CY", 19), ("US", 0), ("XX", -1), (None, -1)]
COUPON_TEXTS = [
    ("# spring\nspring\n\n  Welcome  \n", ["SPRING", "WELCOME"]),
    ("", []),
    ("#only\n#comments\n", []),
]
# name, orders, coupons, mode, expected lines, expected total in cents
ORDERS = [
    ("one plain order", [make("P1", "DE", [("pen", 2, 150)])], [], "text",
     ["order P1 (DE): 8.56 EUR", "total: 8.56 EUR"], 856),
    ("bulk discount at 10 units", [make("P2", "DE", [("pen", 10, 100)])], [], "text",
     ["order P2 (DE): 16.29 EUR", "total: 16.29 EUR"], 1629),
    ("just under the bulk discount", [make("P3", "DE", [("pen", 9, 100)])], [], "text",
     ["order P3 (DE): 15.70 EUR", "total: 15.70 EUR"], 1570),
    ("welcome coupon", [make("P4", "FR", [("pad", 1, 2000)], coupon="WELCOME")], [],
     "text", ["order P4 (FR): 33.59 EUR", "total: 33.59 EUR"], 3359),
    ("list coupon beats welcome", [make("P5", "FR", [("pad", 1, 2000)],
                                        coupon="WELCOME")], ["WELCOME"], "text",
     ["order P5 (FR): 32.39 EUR", "total: 32.39 EUR"], 3239),
    ("unknown coupon", [make("P6", "CY", [("pad", 1, 2000)], coupon="NOPE")], [],
     "text", ["order P6 (CY): 28.79 EUR", "total: 28.79 EUR"], 2879),
    ("bad lines are skipped", [make("P7", "DE", [("a", 0, 100), ("b", 1, 0),
                                                   ("c", 1, 100)])], [], "text",
     ["skip P7: bad quantity for a", "skip P7: bad price for b",
      "order P7 (DE): 6.18 EUR", "total: 6.18 EUR"], 618),
    ("orders that are skipped", [make("P8", "ZZ", [("a", 1, 100)]),
                                 make("P9", "DE", [])], [], "text",
     ["skip P8: unknown country ZZ", "skip P9: no items", "total: 0.00 EUR"], 0),
    ("csv output", [make("P10", "US", [("a", 3, 700)], express=True),
                    make("P11", "DE", [("b", 1, 100)])], [], "csv",
     ["P10,US,42.98", "P11,DE,6.18", "TOTAL,,49.16"], 4916),
    ("free shipping from 50.00", [make("P12", "DE", [("a", 1, 6000)])], [], "text",
     ["order P12 (DE): 71.40 EUR", "total: 71.40 EUR"], 7140),
    ("empty list", [], [], "text", ["total: 0.00 EUR"], 0),
    ("empty list as csv", [], [], "csv", ["TOTAL,,0.00"], 0),
]


class ShippingAndCountry(unittest.TestCase):
    def test_shipping_fees(self):
        for country, subtotal, express, fee in SHIPPING:
            with self.subTest(country=country, subtotal=subtotal, express=express):
                self.assertEqual(quote_shipping(country, subtotal, express), fee)

    def test_country_rates(self):
        for country, rate in COUNTRIES:
            with self.subTest(country=country):
                self.assertEqual(check_country({"country": country}), rate)

    def test_order_without_country_key(self):
        self.assertEqual(check_country({}), -1)

    def test_coupon_files(self):
        for text, expected in COUPON_TEXTS:
            with self.subTest(text=text):
                self.assertEqual(load_coupons(text), expected)


class ProcessOrders(unittest.TestCase):
    def test_orders(self):
        for name, orders, coupons, mode, lines, total in ORDERS:
            with self.subTest(name):
                self.assertEqual(process_orders(orders, coupons, mode),
                                 (lines, total))

    def test_same_input_gives_the_same_output_twice(self):
        orders = ORDERS[3][1]
        self.assertEqual(process_orders(orders), process_orders(orders))

    def test_input_orders_are_not_changed(self):
        orders = [make("Q1", "DE", [("pen", 12, 150)], coupon="WELCOME")]
        copy = [dict(orders[0])]
        process_orders(orders)
        self.assertEqual(orders, copy)


class Summary(unittest.TestCase):
    def test_summary_counts_billed_orders(self):
        orders = [make("S1", "DE", [("a", 1, 1000)]), make("S2", "XX", [("a", 1, 1)]),
                  make("S3", "US", [("a", 2, 1000)])]
        self.assertEqual(summary(orders), "2 of 3 orders billed, 48.88 EUR")

    def test_summary_of_nothing(self):
        self.assertEqual(summary([]), "0 of 0 orders billed, 0.00 EUR")


if __name__ == "__main__":
    unittest.main()
