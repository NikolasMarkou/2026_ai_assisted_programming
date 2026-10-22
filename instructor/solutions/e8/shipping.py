"""Parcel shipping price for a small web shop. Money is in whole cents."""

TIERS = ((2000, 400), (10000, 750), (30000, 1200))  # (heaviest weight in g, price)
FREE_KM = 100
CENTS_PER_KM = 3
EXPRESS_PERCENT = 25
STEP = 5


def shipping_cents(weight_g, distance_km, express=False):
    """Price of one parcel in cents. The rules are in spec.md.

    weight_g: parcel weight in grams, above 0 and at most 30000.
    distance_km: whole kilometres to the destination, 0 or more.
    express: True for next-day delivery.
    Raises ValueError for a weight or distance outside those limits.
    """
    # Rule 2: inputs outside the limits.
    if weight_g <= 0 or distance_km < 0:
        raise ValueError("weight must be above 0 and distance 0 or more")
    # Rule 1: the weight price.
    price = None
    for limit, tier_price in TIERS:
        if weight_g <= limit:
            price = tier_price
            break
    if price is None:
        raise ValueError("parcels above 30000 g are not accepted")
    # Rules 3 and 4: the distance charge and the subtotal.
    subtotal = price + max(0, distance_km - FREE_KM) * CENTS_PER_KM
    # Rule 5: round the subtotal up to a multiple of 5 cents.
    rounded = -(-subtotal // STEP) * STEP
    # Rule 6: the express charge.
    surcharge = 0
    if express:
        surcharge = -(-rounded * EXPRESS_PERCENT // 100)
    # Rule 7: the price.
    return rounded + surcharge
