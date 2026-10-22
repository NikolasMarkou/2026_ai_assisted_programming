"""The frozen evaluator of the E16 ratchet. A proposer must never edit this file.

Usage: python3 prepare.py
It loads candidate.py from its own folder, runs parse_price on the 8 visible cases
below and prints one line per case, then the last line `score: N/8`. Higher is
better. The ratchet reads that last line, the way an agent reads the number a
training run prints.

Interface for other code: load_function(path) returns the parse_price function of a
file (it raises when the file has no such function); grade(function, cases) returns
(passed, total) for a tuple of (text, expected cents or None) pairs. Standard
library only.
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
VISIBLE = (
    ("12", 1200),
    ("$5", 500),
    ("$12.50", 1250),
    ("1,200", 120000),
    ("$1,200.75", 120075),
    ("0.99", 99),
    ("12.50 EUR", 1250),
    ("abc", None),
)


def load_function(path):
    """Import one file by its path and return its parse_price function."""
    spec = importlib.util.spec_from_file_location("candidate", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_price


def results(function, cases):
    """List of (text, expected, got). A case that raises gets got = 'error: Name'."""
    rows = []
    for text, want in cases:
        try:
            got = function(text)
        except Exception as error:  # a broken candidate must not stop the scoring
            got = f"error: {type(error).__name__}"
        rows.append((text, want, got))
    return rows


def tally(rows):
    """Returns (passed, total) for a list made by results()."""
    return sum(got == want for _, want, got in rows), len(rows)


def grade(function, cases):
    """Returns (passed, total) for the given cases."""
    return tally(results(function, cases))


def main():
    function = load_function(HERE / "candidate.py")
    rows = results(function, VISIBLE)
    for number, (text, want, got) in enumerate(rows, 1):
        if got == want:
            print(f"case {number} ok")
        else:
            print(f"case {number} FAIL input {text!r} expected {want!r} got {got!r}")
    passed, total = tally(rows)
    print(f"score: {passed}/{total}")


if __name__ == "__main__":
    main()
