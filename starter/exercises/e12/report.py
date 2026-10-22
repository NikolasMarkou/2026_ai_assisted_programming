"""Text reports for the stock list."""
from inventory import total_value_cents


def money(cents):
    return "%d.%02d" % (cents // 100, cents % 100)


def text_report(items):
    """One line per item and a total line."""
    lines = [f"{i['sku']:7}{i['name']:14}{i['qty']:>4}  {money(i['price_cents'])}"
             for i in items]
    lines.append(f"total value: {money(total_value_cents(items))}")
    return "\n".join(lines)
