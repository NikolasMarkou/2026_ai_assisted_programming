"""Hidden tests for E8. Run from this folder, with the pair's folder on PYTHONPATH:
PYTHONPATH=<the pair's exercises/e8 folder> python3 -B -m unittest -q test_hidden
Never copy this file into the pair's folder.

Test names start with tier_boundary (bug 1) or express_rounding (bug 2).
"""
import unittest

from shipping import shipping_cents


class HiddenShippingTest(unittest.TestCase):
    def test_tier_boundary_2000_g_is_the_lightest_tier(self):
        self.assertEqual(shipping_cents(2000, 0), 400)

    def test_tier_boundary_10000_g_is_the_middle_tier(self):
        self.assertEqual(shipping_cents(10000, 0), 750)

    def test_tier_boundary_30000_g_is_accepted(self):
        self.assertEqual(shipping_cents(30000, 0), 1200)

    def test_tier_boundary_one_gram_over_moves_up(self):
        self.assertEqual(shipping_cents(2001, 0), 750)
        self.assertEqual(shipping_cents(10001, 0), 1200)
        with self.assertRaises(ValueError):
            shipping_cents(30001, 0)

    def test_express_rounding_uses_the_rounded_subtotal(self):
        self.assertEqual(shipping_cents(1500, 127, express=True), 607)

    def test_express_rounding_second_case(self):
        self.assertEqual(shipping_cents(1500, 101, express=True), 507)

    def test_standard_rounding_to_5_cents(self):
        self.assertEqual(shipping_cents(1500, 127), 485)

    def test_free_distance_boundary(self):
        self.assertEqual(shipping_cents(5000, 100), 750)
        self.assertEqual(shipping_cents(5000, 101), 755)

    def test_inputs_outside_the_limits(self):
        for weight, distance in ((0, 5), (-1, 5), (1000, -1)):
            with self.assertRaises(ValueError):
                shipping_cents(weight, distance)


if __name__ == "__main__":
    unittest.main()
