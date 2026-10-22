import unittest

from pricing import order_total_cents


class OrderTotalTest(unittest.TestCase):
    def test_one_line_pays_shipping(self):
        self.assertEqual(order_total_cents([(1000, 2)]), 2000 + 499)

    def test_lines_are_added(self):
        self.assertEqual(order_total_cents([(1000, 1), (250, 4)]), 2000 + 499)

    def test_free_shipping_from_5000(self):
        self.assertEqual(order_total_cents([(2500, 2)]), 5000)

    def test_shipping_just_below_5000(self):
        self.assertEqual(order_total_cents([(4999, 1)]), 4999 + 499)

    def test_bulk_discount_from_10_items(self):
        self.assertEqual(order_total_cents([(100, 10)]), 950 + 499)

    def test_no_bulk_discount_at_9_items(self):
        self.assertEqual(order_total_cents([(100, 9)]), 900 + 499)

    def test_bulk_discount_rounds_down(self):
        self.assertEqual(order_total_cents([(199, 10)]), 1990 - 99 + 499)

    def test_save10_needs_5000(self):
        self.assertEqual(order_total_cents([(2500, 2)], "SAVE10"), 4000 + 499)

    def test_save10_below_the_minimum_does_nothing(self):
        self.assertEqual(order_total_cents([(1000, 1)], "SAVE10"), 1000 + 499)

    def test_save10_uses_the_subtotal_after_bulk(self):
        self.assertEqual(order_total_cents([(500, 10)], "SAVE10"), 4750 + 499)

    def test_freeship_removes_shipping(self):
        self.assertEqual(order_total_cents([(1000, 1)], "FREESHIP"), 1000)

    def test_unknown_coupon(self):
        with self.assertRaises(ValueError):
            order_total_cents([(1000, 1)], "HALF")

    def test_empty_basket(self):
        with self.assertRaises(ValueError):
            order_total_cents([])

    def test_bad_lines(self):
        for line in ((0, 1), (-5, 1), (100, 0), (100, 100)):
            with self.assertRaises(ValueError):
                order_total_cents([line])


if __name__ == "__main__":
    unittest.main()
