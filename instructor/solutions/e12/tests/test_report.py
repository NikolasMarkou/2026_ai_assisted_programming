import io
import unittest

import cli
from inventory import ITEMS, low_stock, total_value_cents
from report import money, text_report, to_csv


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


class Export(unittest.TestCase):
    def test_header_and_row_count(self):
        lines = to_csv(ITEMS).splitlines()
        self.assertEqual(lines[0], "sku,name,qty,price")
        self.assertEqual(len(lines), len(ITEMS) + 1)

    def test_name_with_a_comma_is_quoted(self):
        self.assertIn('A-200,"Pen, blue",8,1.20', to_csv(ITEMS))

    def test_price_has_2_decimals(self):
        self.assertIn("B-300,Desk lamp,3,24.99", to_csv(ITEMS).splitlines())

    def test_export_command(self):
        out = io.StringIO()
        self.assertEqual(cli.main(["export"], out), 0)
        self.assertEqual(out.getvalue(), to_csv(ITEMS))

    def test_export_low_keeps_the_low_order(self):
        out = io.StringIO()
        cli.main(["export", "--low", "9"], out)
        self.assertEqual([l[:5] for l in out.getvalue().splitlines()[1:]],
                         ["C-500", "B-300", "A-200"])


if __name__ == "__main__":
    unittest.main()
