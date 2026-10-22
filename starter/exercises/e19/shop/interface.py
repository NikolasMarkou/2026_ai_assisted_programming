"""The shared interface of the order package. Only the planner may change this file.

Line is one order line. money(cents) is the one place that writes an amount as text.
Every slice imports from here, so a change here can break all three slices at once.
"""
from collections import namedtuple

Line = namedtuple("Line", "name qty cents")


def money(cents):
    """Write whole cents as text with two decimals: 12305 gives '123.05'."""
    return f"{cents // 100}.{cents % 100:02d}"
