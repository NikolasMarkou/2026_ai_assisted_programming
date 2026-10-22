"""Scripted agents for exercise E20. No model runs: each agent is a fixed script.

An agent is a function agent(ws) that edits files in the worktree folder ws and returns
one handoff line. It does not commit: the driver commits what the agent left.
  BEST_OF_N      two agents that solve the same task (initials in names.py)
  PAIRS          three pairs of agents that solve two different tasks on one base
  leaky_agent    the agent of not_a_sandbox.py, which also writes outside its folder
Standard library only.
"""
import subprocess


def write(ws, name, text):
    (ws / name).write_text(text, encoding="utf-8")


def edit(ws, name, old, new):
    """Replace old by new in a file of ws. ValueError when old is not in the file."""
    text = (ws / name).read_text(encoding="utf-8")
    if old not in text:
        raise ValueError(f"{name} does not contain {old!r}")
    write(ws, name, text.replace(old, new))


# ---- one task, two agents (best-of-N)
def initials_any_space(ws):
    edit(ws, "names.py", "    raise NotImplementedError",
         '    return "".join(word[0].upper() for word in name.split())')
    return "split on any run of whitespace, upper-case the first letter of each word"


def initials_single_space(ws):
    edit(ws, "names.py", "    raise NotImplementedError",
         '    if not name:\n        return ""\n'
         '    return "".join(word[0].upper() for word in name.split(" "))')
    return "split on single spaces, upper-case the first letter, empty input gives ''"


BEST_OF_N = {"agent-a": initials_any_space, "agent-b": initials_single_space}

# ---- two tasks, two agents, one base (merge order)
DISCOUNT_TEST = '''import unittest

from discount import apply_discount


class TestDiscount(unittest.TestCase):
    def test_ten_percent(self):
        self.assertEqual(apply_discount(1000, 10), 900)

    def test_no_discount(self):
        self.assertEqual(apply_discount(1000, 0), 1000)
'''
RECEIPT = '''import prices


def receipt(items):
    lines = [f"{item} {prices.price(item)}" for item in items]
    return "\\n".join(lines + [f"total {prices.total(items)}"])
'''
RECEIPT_TEST = '''import unittest

from receipt import receipt


class TestReceipt(unittest.TestCase):
    def test_one_item(self):
        self.assertEqual(receipt(["pen"]), "pen 120\\ntotal 120")

    def test_no_items(self):
        self.assertEqual(receipt([]), "total 0")
'''
BULK_TEST = '''import unittest

from prices import total


class TestBulk(unittest.TestCase):
    def test_three_items_get_ten_percent_off(self):
        self.assertEqual(total(["pen", "pen", "pen"]), 324)
'''
SHIPPING_TEST = '''import unittest

from prices import total


class TestShipping(unittest.TestCase):
    def test_shipping_is_added(self):
        self.assertEqual(total(["pen"]), 620)
'''
SUM_LINE = "    return sum(price(item) for item in items)"


def add_discount(ws):
    write(ws, "discount.py", "def apply_discount(cents, percent):\n"
          "    return cents - cents * percent // 100\n")
    write(ws, "test_discount.py", DISCOUNT_TEST)
    return "new file discount.py with apply_discount, 2 tests"


def add_receipt(ws):
    write(ws, "receipt.py", RECEIPT)
    write(ws, "test_receipt.py", RECEIPT_TEST)
    return "new file receipt.py that prints each price and the total, 2 tests"


def bulk_discount(ws):
    edit(ws, "prices.py", SUM_LINE, "    cents = sum(price(item) for item in items)\n"
         "    return cents * 9 // 10 if len(items) >= 3 else cents")
    write(ws, "test_bulk.py", BULK_TEST)
    return "total() takes 10 percent off a basket of 3 or more items, 1 test"


def add_shipping(ws):
    edit(ws, "prices.py", SUM_LINE, "    cents = sum(price(item) for item in items)\n"
         "    return cents + 500 if items else 0")
    edit(ws, "test_prices.py", "1070", "1570")
    write(ws, "test_shipping.py", SHIPPING_TEST)
    return "total() adds 500 cents of shipping to a basket that is not empty, 1 test"


def rename_price(ws):
    edit(ws, "prices.py", "price(", "unit_price(")
    edit(ws, "test_prices.py", "import price, total", "import total, unit_price")
    edit(ws, "test_prices.py", 'price("pen")', 'unit_price("pen")')
    return "price() renamed unit_price() in prices.py and its test"


PAIRS = [
    ("different files", {"agent-a": add_discount, "agent-b": add_receipt}),
    ("the same file", {"agent-a": bulk_discount, "agent-b": add_shipping}),
    ("different files, one breaks the other", {"agent-a": rename_price,
                                               "agent-b": add_receipt}),
]


# ---- the agent that is not in a sandbox
def leaky_agent(ws, main):
    """Edit notes.txt in ws as asked, then write into the folder main by absolute path.

    Runs the three shell commands with ws as the current directory and returns them,
    with the path of main replaced by <main checkout>.
    """
    commands = ['echo "edited in the worktree" >> notes.txt',
                f'echo "written from the worktree" >> "{main}/config.txt"',
                f'echo "a new file" > "{main}/leak.txt"']
    for command in commands:
        subprocess.run(command, shell=True, cwd=ws, check=True)
    return [command.replace(str(main), "<main checkout>") for command in commands]
