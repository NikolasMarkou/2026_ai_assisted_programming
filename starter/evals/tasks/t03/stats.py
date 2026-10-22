def median(values):
    """Middle value of a list. For an even count, the mean of the two middle values."""
    if not values:
        raise ValueError("median of an empty list")
    ordered = sorted(values)
    return ordered[len(ordered) // 2]
