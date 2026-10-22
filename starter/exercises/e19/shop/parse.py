"""Slice a: read an order from text. Owned by worker a."""
from shop.interface import Line


def parse_order(text):
    """Turn lines such as '2 x red pen @ 1.50' into Line(name, qty, cents) values.

    Empty lines are skipped. The price has at most 2 decimals and is read as text,
    not as a float: '0.29' gives 29 cents.
    """
    raise NotImplementedError("slice a: write parse_order")
