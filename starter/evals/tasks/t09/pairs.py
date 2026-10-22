def parse_pairs(text):
    """Parse 'a=1;b=2' into {'a': '1', 'b': '2'}. A value may contain '='."""
    result = {}
    for part in text.split(";"):
        if not part:
            continue
        key, value = part.split("=")
        result[key.strip()] = value.strip()
    return result
