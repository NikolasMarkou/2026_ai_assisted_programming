BULK_ITEMS = 10
BULK_PERCENT = 5
SAVE10_OFF = 1000
SAVE10_MINIMUM = 5000
FREE_SHIPPING_FROM = 5000
SHIPPING_CENTS = 499
COUPONS = (None, "SAVE10", "FREESHIP")


def order_total_cents(lines, coupon=None):
    """Total price of a basket in whole cents. The rules are in spec.md.

    lines: a list of (unit_cents, quantity) pairs.
    coupon: None, "SAVE10" or "FREESHIP".
    Raises ValueError for an invalid basket line, an empty basket or an unknown coupon.
    """
    if not lines or coupon not in COUPONS:
        raise ValueError("empty basket or unknown coupon")
    subtotal = items = 0
    for unit_cents, quantity in lines:
        if unit_cents <= 0 or not 1 <= quantity <= 99:
            raise ValueError(f"bad line: {unit_cents} x {quantity}")
        subtotal += unit_cents * quantity
        items += quantity
    if items >= BULK_ITEMS:
        subtotal -= subtotal * BULK_PERCENT // 100
    if coupon == "SAVE10" and subtotal >= SAVE10_MINIMUM:
        subtotal -= SAVE10_OFF
    shipping = SHIPPING_CENTS
    if coupon == "FREESHIP" or subtotal >= FREE_SHIPPING_FROM:
        shipping = 0
    return subtotal + shipping
