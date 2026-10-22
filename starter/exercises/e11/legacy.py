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


def process_orders(orders, coupons=[], mode="text"):
    """Return (lines, grand_total_cents) for a list of order dicts.

    An order has id, country, items [(sku, qty, unit_cents)], coupon, express.
    """
    lines = []
    total = 0
    for o in orders:
        oid = o["id"]
        if o.get("items"):
            rate = check_country(o)
            if rate >= 0:
                sub = 0
                for it in o["items"]:
                    if it[1] > 0:
                        if it[2] > 0:
                            line = it[1] * it[2]
                            if it[1] >= 10:
                                line = line - line * 5 // 100
                            sub = sub + line
                        else:
                            lines.append("skip %s: bad price for %s" % (oid, it[0]))
                    else:
                        lines.append("skip %s: bad quantity for %s" % (oid, it[0]))
                disc = 0
                code = o.get("coupon")
                if code:
                    if code in coupons:
                        disc = sub * 15 // 100
                    elif code == "WELCOME":
                        disc = sub * 10 // 100
                net = sub - disc
                tax = net * rate // 100
                ship = quote_shipping(o["country"], net, o.get("express", False))
                value = net + tax + ship
                total = total + value
                euros = value // 100
                rest = value % 100
                money = "%d.%02d" % (euros, rest)
                if mode == "csv":
                    lines.append("%s,%s,%s" % (oid, o["country"], money))
                else:
                    lines.append("order %s (%s): %s EUR" % (oid, o["country"], money))
            else:
                lines.append("skip %s: unknown country %s" % (oid, o["country"]))
        else:
            lines.append("skip %s: no items" % oid)
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
