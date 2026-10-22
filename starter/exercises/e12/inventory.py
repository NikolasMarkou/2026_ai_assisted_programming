"""A tiny stock list. The data is in the code, so the exercise needs no files."""

ITEMS = [
    {"sku": "A-100", "name": "Notebook", "qty": 40, "price_cents": 350},
    {"sku": "A-200", "name": "Pen, blue", "qty": 8, "price_cents": 120},
    {"sku": "B-300", "name": "Desk lamp", "qty": 3, "price_cents": 2499},
    {"sku": "B-400", "name": "Mug, 300 ml", "qty": 25, "price_cents": 899},
    {"sku": "C-500", "name": "Cable, 2 m", "qty": 0, "price_cents": 650},
]


def low_stock(items, limit=10):
    """Return the items whose quantity is below limit, lowest quantity first."""
    return sorted((i for i in items if i["qty"] < limit), key=lambda i: i["qty"])


def total_value_cents(items):
    return sum(i["qty"] * i["price_cents"] for i in items)
