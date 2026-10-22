def percent(part, total):
    """part as a percentage of total, rounded to 1 decimal. 0.0 when total is 0."""
    return round(100 * part / total, 1)
