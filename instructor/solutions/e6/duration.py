import re

UNITS = {"h": 3600, "m": 60, "s": 1}


def parse_duration(text):
    """Convert a duration such as '1h30m' to whole seconds.

    The text is one or more parts. A part is a whole number followed by one unit:
    h (hours), m (minutes) or s (seconds). Parts may appear in any order and are added.
    Raises ValueError for empty text, a number without a unit, or an unknown unit.

    >>> parse_duration("1h30m")
    5400
    >>> parse_duration("45s")
    45
    >>> parse_duration("2m10s")
    130
    """
    if not re.fullmatch(r"(\d+[hms])+", text):
        raise ValueError(f"not a duration: {text!r}")
    return sum(int(n) * UNITS[unit] for n, unit in re.findall(r"(\d+)([hms])", text))
