"""Text reports for the stock list."""
import csv
import io

from inventory import total_value_cents


def money(cents):
    return "%d.%02d" % (cents // 100, cents % 100)


def text_report(items):
    """One line per item and a total line."""
    lines = [f"{i['sku']:7}{i['name']:14}{i['qty']:>4}  {money(i['price_cents'])}"
             for i in items]
    lines.append(f"total value: {money(total_value_cents(items))}")
    return "\n".join(lines)


def to_csv(items):
    """CSV text: header sku,name,qty,price, then one row per item, lines end in \\n."""
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(["sku", "name", "qty", "price"])
    for i in items:
        writer.writerow([i["sku"], i["name"], i["qty"], money(i["price_cents"])])
    return out.getvalue()
