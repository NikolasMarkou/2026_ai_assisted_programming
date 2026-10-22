"""Slice c: the text of a receipt. Owned by worker c."""
from shop.interface import Line, money


def receipt(lines, total_cents):
    """One text line per order line, then the total, joined by newlines.

    Each order line reads '<name> x<qty>: <qty * cents as money>'. The last line
    reads 'TOTAL: <total as money>'. There is no newline at the end.
    """
    raise NotImplementedError("slice c: write receipt")
