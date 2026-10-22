import unittest

from pages import page_count


class HiddenPageCountTest(unittest.TestCase):
    def test_one_item(self):
        self.assertEqual(page_count(1, 10), 1)

    def test_one_over(self):
        self.assertEqual(page_count(101, 100), 2)

    def test_no_items(self):
        self.assertEqual(page_count(0, 5), 0)

    def test_per_page_below_one_is_rejected(self):
        with self.assertRaises(ValueError):
            page_count(5, 0)
