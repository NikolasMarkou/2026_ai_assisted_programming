import unittest

from pages import page_count


class PageCountTest(unittest.TestCase):
    def test_exact_pages(self):
        self.assertEqual(page_count(20, 10), 2)

    def test_partial_last_page(self):
        self.assertEqual(page_count(21, 10), 3)
