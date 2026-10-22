"""Prove that recorded test files were not edited, without git.

Usage: python3 check_untouched.py record TESTS_DIR [--hashes FILE]
       python3 check_untouched.py check TESTS_DIR [--hashes FILE]
`record` writes the sha256 of every .py file under TESTS_DIR, right after you save the
tests. It refuses to overwrite an existing hash file. `check` compares the files with
that record: EDITED and DELETED files make the exit code 1; NEW files are listed and
allowed, because adding tests is the point of coverage-driven prompting.
A hash file in the same folder can be edited by anyone who can edit the tests. Keep a
copy outside the project, or use git. Standard library only.
"""
import argparse
import hashlib
import sys
from pathlib import Path

DEFAULT_HASHES = "committed_tests.sha256"


def hash_tree(folder):
    """Dict of relative path -> sha256 for every .py file under folder."""
    return {str(path.relative_to(folder)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(folder.rglob("*.py")) if "__pycache__" not in path.parts}


def compare(recorded, current):
    """Returns (edited, deleted, new): three sorted lists of relative paths."""
    edited = [p for p in recorded if p in current and recorded[p] != current[p]]
    deleted = [p for p in recorded if p not in current]
    new = [p for p in current if p not in recorded]
    return sorted(edited), sorted(deleted), sorted(new)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("mode", choices=("record", "check"))
    parser.add_argument("folder")
    parser.add_argument("--hashes", default=DEFAULT_HASHES)
    args = parser.parse_args()
    folder, hashes = Path(args.folder), Path(args.hashes)
    current = hash_tree(folder)
    if args.mode == "record":
        if hashes.exists():
            print(f"{hashes} exists: refusing to overwrite it")
            return 2
        hashes.write_text("".join(f"{h}  {p}\n" for p, h in current.items()))
        print(f"recorded {len(current)} files in {hashes}")
        return 0
    if not hashes.exists():
        print(f"{hashes} not found: run `record` right after you save the tests")
        return 2
    recorded = {line.split("  ", 1)[1]: line.split("  ", 1)[0]
                for line in hashes.read_text().splitlines() if line}
    edited, deleted, new = compare(recorded, current)
    for label, paths in (("EDITED", edited), ("DELETED", deleted), ("NEW", new)):
        for path in paths:
            print(f"{label}  {path}")
    print(f"{len(recorded) - len(edited) - len(deleted)} of {len(recorded)} "
          "recorded files unchanged")
    return 1 if edited or deleted else 0


if __name__ == "__main__":
    sys.exit(main())
