"""The one file a proposer may edit in the E16 ratchet."""


def parse_price(text):
    """Return the price in cents as an int, or None when text is not a price."""
    text = text.strip()
    if not text.isdigit():
        return None
    return int(text) * 100
