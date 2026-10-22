import unittest

from shipping import shipping_cents


class ShippingTest(unittest.TestCase):
    def test_light_parcel_nearby(self):
        self.assertEqual(shipping_cents(1500, 0), 400)

    def test_medium_parcel(self):
        self.assertEqual(shipping_cents(5000, 50), 750)

    def test_heavy_parcel(self):
        self.assertEqual(shipping_cents(12000, 0), 1200)

    def test_long_distance_adds_3_cents_per_km_after_100(self):
        self.assertEqual(shipping_cents(5000, 150), 900)

    def test_express_adds_a_quarter(self):
        self.assertEqual(shipping_cents(1500, 0, express=True), 500)

    def test_express_with_distance(self):
        self.assertEqual(shipping_cents(5000, 150, express=True), 1125)

    def test_zero_weight_is_rejected(self):
        with self.assertRaises(ValueError):
            shipping_cents(0, 10)

    def test_too_heavy_is_rejected(self):
        with self.assertRaises(ValueError):
            shipping_cents(40000, 10)


if __name__ == "__main__":
    unittest.main()
