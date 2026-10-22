"""Line coverage of one module with the standard library: which lines did the tests run.

Usage: python3 cov.py MODULE.py [--tests tests] [--min 90]
Runs the unittest tests found in --tests (default: tests) inside this process, records
which lines of MODULE.py ran, and prints the percentage and the line numbers that did
not run. Exit code 1 when a test fails or the percentage is below --min.

This is LINE coverage: a statement counts when its first line ran at least once. It does
not record branches, so `if x: a()` counts as covered when the condition was true and
the false side never ran. The real tool for that is optional:
    coverage run --branch -m unittest -q && coverage report -m
Standard library only.
"""
import argparse
import ast
import io
import sys
import unittest
from pathlib import Path


def executable_lines(path):
    """Set of line numbers where a statement starts, docstrings left out."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)):
            first = node.body[0] if node.body else None
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                docstrings.add(first.lineno)
    return {n.lineno for n in ast.walk(tree) if isinstance(n, ast.stmt)} - docstrings


def run_traced(path, tests_dir):
    """Run the tests with a line tracer. Returns (lines that ran, unittest result)."""
    target, ran, cache = str(path.resolve()), set(), {}

    def tracer(frame, event, arg):
        code = frame.f_code
        if cache.setdefault(code, str(Path(code.co_filename).resolve()) == target):
            if event == "line":
                ran.add(frame.f_lineno)
            return tracer
        return None

    sys.path.insert(0, str(path.resolve().parent))
    sys.settrace(tracer)  # before discovery: importing the tests imports the module
    try:
        suite = unittest.defaultTestLoader.discover(
            str(tests_dir), top_level_dir=str(path.resolve().parent))
        result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    finally:
        sys.settrace(None)
    return ran, result


def as_ranges(numbers):
    """[3, 4, 5, 9] -> '3-5, 9'."""
    parts, numbers = [], sorted(numbers)
    while numbers:
        end = start = numbers.pop(0)
        while numbers and numbers[0] == end + 1:
            end = numbers.pop(0)
        parts.append(str(start) if start == end else f"{start}-{end}")
    return ", ".join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("module")
    parser.add_argument("--tests", default="tests")
    parser.add_argument("--min", type=float, default=0.0, help="minimum percent")
    args = parser.parse_args()
    path = Path(args.module)
    wanted = executable_lines(path)
    ran, result = run_traced(path, Path(args.tests))
    missed = wanted - ran
    percent = 100 * (len(wanted) - len(missed)) / len(wanted)
    bad = len(result.failures) + len(result.errors)
    print(f"tests: {result.testsRun} run, {bad} failed")
    print(f"{path.name}: {len(wanted) - len(missed)} of {len(wanted)} lines ran "
          f"({percent:.0f}%)")
    print("lines that did not run: " + (as_ranges(missed) or "none"))
    print("line coverage only; branch coverage needs `coverage run --branch`")
    return 1 if bad or percent < args.min else 0


if __name__ == "__main__":
    sys.exit(main())
