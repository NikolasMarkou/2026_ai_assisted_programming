import io
import unittest

import cli
from inventory import ITEMS, low_stock, total_value_cents
from report import money, text_report


class Inventory(unittest.TestCase):
    def test_low_stock_is_sorted_by_quantity(self):
        skus = [i["sku"] for i in low_stock(ITEMS)]
        self.assertEqual(skus, ["C-500", "B-300", "A-200"])

    def test_low_stock_limit(self):
        self.assertEqual([i["sku"] for i in low_stock(ITEMS, 4)], ["C-500", "B-300"])

    def test_total_value(self):
        self.assertEqual(total_value_cents(ITEMS), 14000 + 960 + 7497 + 22475)


class Report(unittest.TestCase):
    def test_money(self):
        self.assertEqual(money(5), "0.05")
        self.assertEqual(money(2499), "24.99")

    def test_text_report_ends_with_the_total(self):
        self.assertEqual(text_report(ITEMS).splitlines()[-1], "total value: 449.32")

    def test_text_report_has_one_line_per_item(self):
        self.assertEqual(len(text_report(ITEMS).splitlines()), len(ITEMS) + 1)


class Cli(unittest.TestCase):
    def test_report_command(self):
        out = io.StringIO()
        self.assertEqual(cli.main(["report"], out), 0)
        self.assertIn("Notebook", out.getvalue())

    def test_low_command_with_limit(self):
        out = io.StringIO()
        cli.main(["low", "--limit", "1"], out)
        self.assertIn("Cable", out.getvalue())
        self.assertNotIn("Notebook", out.getvalue())


if __name__ == "__main__":
    unittest.main()
