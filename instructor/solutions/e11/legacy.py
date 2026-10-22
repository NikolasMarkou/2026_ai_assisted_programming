"""Order handling for a small web shop. Written in a hurry, never cleaned up."""

TAX = {"DE": 19, "FR": 20, "CY": 19, "US": 0}


def check_country(order):
    rate = TAX.get(order.get("country"))
    if rate is None:
        return -1
    return rate


def load_coupons(text):
    found = []
    for row in text.splitlines():
        row = row.strip()
        if row and not row.startswith("#"):
            found.append(row.upper())
    return found


def quote_shipping(country, subtotal, express=False):
    if subtotal >= 5000:
        fee = 0
    else:
        fee = 499
    if country != "DE" and country != "CY":
        fee = fee + 700
    if express:
        fee = fee + 999
    return fee


def _price_items(oid, items, lines):
    """Return the item subtotal in cents; add one skip line per unusable item."""
    sub = 0
    for it in items:
        if it[1] <= 0:
            lines.append("skip %s: bad quantity for %s" % (oid, it[0]))
        elif it[2] <= 0:
            lines.append("skip %s: bad price for %s" % (oid, it[0]))
        else:
            line = it[1] * it[2]
            if it[1] >= 10:
                line = line - line * 5 // 100
            sub = sub + line
    return sub


def _discount(code, sub, coupons):
    if code and code in coupons:
        return sub * 15 // 100
    if code and code == "WELCOME":
        return sub * 10 // 100
    return 0


def _bill_order(o, rate, coupons, mode, lines):
    """Add the order's lines to lines and return what the customer pays in cents."""
    sub = _price_items(o["id"], o["items"], lines)
    net = sub - _discount(o.get("coupon"), sub, coupons)
    tax = net * rate // 100
    ship = quote_shipping(o["country"], net, o.get("express", False))
    value = net + tax + ship
    euros = value // 100
    rest = value % 100
    money = "%d.%02d" % (euros, rest)
    if mode == "csv":
        lines.append("%s,%s,%s" % (o["id"], o["country"], money))
    else:
        lines.append("order %s (%s): %s EUR" % (o["id"], o["country"], money))
    return value


def process_orders(orders, coupons=[], mode="text"):
    """Return (lines, grand_total_cents) for a list of order dicts.

    An order has id, country, items [(sku, qty, unit_cents)], coupon, express.
    """
    lines = []
    total = 0
    for o in orders:
        rate = check_country(o)
        if not o.get("items"):
            lines.append("skip %s: no items" % o["id"])
        elif rate < 0:
            lines.append("skip %s: unknown country %s" % (o["id"], o["country"]))
        else:
            total = total + _bill_order(o, rate, coupons, mode, lines)
    value = total
    euros = value // 100
    rest = value % 100
    money = "%d.%02d" % (euros, rest)
    if mode == "csv":
        lines.append("TOTAL,,%s" % money)
    else:
        lines.append("total: %s EUR" % money)
    return lines, total


def summary(orders):
    lines, total = process_orders(orders)
    good = 0
    for text in lines:
        if text.startswith("order"):
            good = good + 1
    value = total
    euros = value // 100
    rest = value % 100
    money = "%d.%02d" % (euros, rest)
    return "%d of %d orders billed, %s EUR" % (good, len(orders), money)
