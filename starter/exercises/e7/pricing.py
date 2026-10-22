def order_total_cents(lines, coupon=None):
    """Total price of a basket in whole cents. The rules are in spec.md.

    lines: a list of (unit_cents, quantity) pairs.
    coupon: None, "SAVE10" or "FREESHIP".
    Raises ValueError for an invalid basket line, an empty basket or an unknown coupon.
    """
    raise NotImplementedError
