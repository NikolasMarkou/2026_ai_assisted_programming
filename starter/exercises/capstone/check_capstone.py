"""Check the capstone: the tests pass and PR_DESCRIPTION.md is filled in.

    python3 check_capstone.py [PR_DESCRIPTION.md]

Checks: (1) python3 -m unittest -q passes in this folder; (2) the description has the 4
part headings (model, harness, sandbox, knowledge and tools), each with at least 5 words
of your own text and no TODO left; (3) the section "What I verified" lists at least 3
lines that start with "- "; (4) the sections "What the AI did" and "The feature" are
filled. Exit 0 when all pass, 1 when one fails. It does not check whether what you wrote
is true: your reviewer reads it. Standard library only.
"""
import re
import subprocess
import sys
from pathlib import Path

PARTS = ["model", "harness", "sandbox", "knowledge and tools"]
SECTIONS = ["The feature", "What the AI did"]
MIN_WORDS = 5
MIN_STEPS = 3


def sections(text):
    """Map each heading (any level) to the text under it, up to the next heading."""
    parts = re.split(r"^#{1,6} +(.+?) *$", text, flags=re.M)
    return {parts[i].strip(): parts[i + 1] for i in range(1, len(parts) - 1, 2)}


def filled(body):
    """True when the body has enough words and no TODO."""
    return "TODO" not in body and len(body.split()) >= MIN_WORDS


def problems_in(text):
    """Return a list of messages, one per missing or empty part."""
    found, problems = sections(text), []
    for name in PARTS + SECTIONS:
        if name not in found:
            problems.append(f"missing heading: {name}")
        elif not filled(found[name]):
            problems.append(f"empty or TODO: {name}")
    steps = [l for l in found.get("What I verified", "").splitlines()
             if l.startswith("- ") and "TODO" not in l and len(l.split()) > 2]
    if len(steps) < MIN_STEPS:
        problems.append(f"What I verified lists {len(steps)} steps, need {MIN_STEPS}")
    return problems


def main(argv):
    tests = subprocess.run([sys.executable, "-m", "unittest", "-q"],
                           capture_output=True, text=True)
    print(("PASS" if tests.returncode == 0 else "FAIL") + "  tests: "
          + (tests.stderr.strip().splitlines() or [""])[-1])
    path = Path(argv[0] if argv else "PR_DESCRIPTION.md")
    if not path.exists():
        print(f"FAIL  {path} does not exist")
        return 1
    problems = problems_in(path.read_text(encoding="utf-8"))
    for message in problems:
        print(f"FAIL  {message}")
    if not problems:
        print(f"PASS  {path}: 4 parts, features, AI steps and {MIN_STEPS}+ checks")
    return 0 if tests.returncode == 0 and not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
