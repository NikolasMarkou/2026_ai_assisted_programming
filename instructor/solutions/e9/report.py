"""Nightly sensor report.

summary(rows) takes (day, value) pairs and returns the number of days seen and the
mean of the daily means. A value of None means the sensor sent nothing that time.
With no usable rows the report is {"days": 0, "mean": None}.
"""


def usable(rows):
    """Rows whose value is not None."""
    return [(day, value) for day, value in rows if value is not None]


def mean_per_day(by_day):
    """Mean of the daily means. by_day maps a day to a list of values."""
    daily = [sum(values) / len(values) for values in by_day.values()]
    return sum(daily) / len(by_day)


def summary(rows):
    """Report for one night: {"days": int, "mean": float or None}."""
    by_day = {}
    for day, value in usable(rows):
        by_day.setdefault(day, []).append(value)
    if not by_day:
        return {"days": 0, "mean": None}
    return {"days": len(by_day), "mean": round(mean_per_day(by_day), 2)}
