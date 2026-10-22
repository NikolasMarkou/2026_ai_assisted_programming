"""Check a README section against the code it describes.

    python3 check_readme.py legacy.py README_section.md

A function mention is a backticked name followed by (), for example `quote_shipping()`.
Rule 1: every mentioned function must exist in the code (a def anywhere in the file).
Rule 2: every public function (a def at module level, name not starting with _) must
be mentioned in backticks, with or without (). Exit 0 when both hold, 1 when not,
2 on a usage error. Standard library only.
"""
import ast
import re
import sys
from pathlib import Path


def defined_names(source):
    """Return (all function names, public module-level function names)."""
    tree = ast.parse(source)
    every = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    public = {n.name for n in tree.body
              if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")}
    return every, public


def mentions(text):
    """Return (names written as `name()`, all backticked identifiers)."""
    called = set(re.findall(r"`([A-Za-z_]\w*)\(\)`", text))
    ticked = set(re.findall(r"`([A-Za-z_]\w*)(?:\(\))?`", text))
    return called, ticked


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    every, public = defined_names(Path(argv[0]).read_text(encoding="utf-8"))
    called, ticked = mentions(Path(argv[1]).read_text(encoding="utf-8"))
    invented = sorted(called - every)
    missing = sorted(public - ticked)
    print(f"public functions in the code: {len(public)}")
    print(f"functions the README names with (): {len(called)}")
    for name in invented:
        print(f"FAIL  the README names {name}() but the code has no such function")
    for name in missing:
        print(f"FAIL  public function {name} is not mentioned in the README")
    print("RESULT: " + ("PASS" if not invented and not missing else "FAIL"))
    return 1 if invented or missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
