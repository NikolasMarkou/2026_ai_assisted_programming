"""Tests for the order package. One test class per slice; they do not use each other.

TestParse needs parse.py, TestTotal needs total.py and TestRender needs render.py.
Each class builds its input by hand from the shared interface. No worker edits this
file: it belongs to the planner.
"""
import unittest

from shop import parse, render, total
from shop.interface import Line


class TestParse(unittest.TestCase):
    def test_one_line(self):
        self.assertEqual(parse.parse_order("2 x red pen @ 1.50"),
                         [Line("red pen", 2, 150)])

    def test_empty_lines_are_skipped(self):
        self.assertEqual(parse.parse_order("\n1 x ink @ 12.00\n\n"),
                         [Line("ink", 1, 1200)])

    def test_price_is_read_as_text(self):
        self.assertEqual(parse.parse_order("3 x clip @ 0.29")[0].cents, 29)


class TestTotal(unittest.TestCase):
    def test_sum_without_discount(self):
        self.assertEqual(total.order_total([Line("pen", 2, 150), Line("ink", 1, 800)]),
                         1100)

    def test_ten_percent_off_from_100_00(self):
        self.assertEqual(total.order_total([Line("desk", 1, 12345)]), 11111)

    def test_just_below_the_limit(self):
        self.assertEqual(total.order_total([Line("lamp", 1, 9999)]), 9999)


class TestRender(unittest.TestCase):
    def test_lines_and_total(self):
        lines = [Line("red pen", 2, 150), Line("ink", 1, 1205)]
        self.assertEqual(render.receipt(lines, 1505),
                         "red pen x2: 3.00\nink x1: 12.05\nTOTAL: 15.05")

    def test_zero_padded_cents(self):
        self.assertEqual(render.receipt([Line("clip", 3, 3)], 9),
                         "clip x3: 0.09\nTOTAL: 0.09")

    def test_empty_order(self):
        self.assertEqual(render.receipt([], 0), "TOTAL: 0.00")
