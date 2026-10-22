def chunk(items, size):
    """Split a list into lists of at most size items. The last one may be shorter."""
    if size < 1:
        raise ValueError("size must be 1 or more")
    return [items[i:i + size] for i in range(0, len(items) - size + 1, size)]
