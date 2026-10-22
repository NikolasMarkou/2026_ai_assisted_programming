"""Slice b: the total of an order. Owned by worker b."""
from shop.interface import Line


def order_total(lines):
    """The total in whole cents: the sum of qty * cents over all lines.

    When that sum is 10000 cents (100.00) or more, take 10 percent off the whole
    order. Use integer arithmetic: the discount is sum // 10 cents, dropped from
    the sum, so 12345 gives 11111.
    """
    raise NotImplementedError("slice b: write order_total")
