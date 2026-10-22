"""Command line for the stock list: python3 cli.py report | low."""
import argparse
import sys

from inventory import ITEMS, low_stock
from report import text_report


def main(argv, out=sys.stdout):
    parser = argparse.ArgumentParser(prog="cli.py")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("report", help="print every item and the total value")
    low = sub.add_parser("low", help="print the items that are low on stock")
    low.add_argument("--limit", type=int, default=10)
    args = parser.parse_args(argv)
    if args.command == "report":
        print(text_report(ITEMS), file=out)
    else:
        print(text_report(low_stock(ITEMS, args.limit)), file=out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
