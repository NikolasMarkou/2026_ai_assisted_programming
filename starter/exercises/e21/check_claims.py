"""Check the claims in a pull request text: does each one come with evidence?

Usage: python3 exercises/e21/check_claims.py FOLDER_OR_PR_TEXT
FOLDER holds pr_text.md (the description), diff.patch (the change) and the files the
diff names. Give pr_text.md instead of the folder and its folder is used.
A claim is a line that starts with `tests`, `covers` or `fixes` (after an optional
bullet mark), and the indented lines under it. A claim has evidence when its lines hold
either of these:
  * a test name (test_something) and every test name in it is defined (`def test_...`)
    in a file the diff changes;
  * a pasted command output: a line that starts with `$ ` and then a line of output.
A claim with neither is flagged. A claim that names a test the changed files do not
define is flagged, even when it also names a test that exists.
Exit code 0 when every claim has evidence, 1 when a claim is flagged, 2 when a file
cannot be read. The output shows file names only, so it is the same on every machine.
What the check cannot see: whether a pasted output is real (it does not run the
command), whether a test passes, or whether a test checks what the claim says. It reads
the shape of the text. Run the tests yourself.
Interface for other code: claims(text) returns [(first line, [more lines])];
changed_files(diff_text) returns the file names after `+++ b/`;
test_names(text) returns the names defined with `def test_...`;
judge(claim, defined) returns (flagged, note) for one claim.
Standard library only.
"""
import re
import sys
from pathlib import Path

CLAIM = re.compile(r"^\s*(?:[-*]\s+)?(tests|covers|fixes)\b[:\s]", re.I)
BULLET = re.compile(r"^[-*]\s")
BULLET_MARK = re.compile(r"^[-*]\s+")
TEST_NAME = re.compile(r"\btest_\w+")
DEFINED = re.compile(r"^\s*def (test_\w+)\(", re.M)
PASTED = re.compile(r"^\s*\$ \S")


def claims(text):
    """[(first line, [following lines])] for every claim in the text.

    A claim runs on while the next lines are indented or inside a ``` fence. A blank
    line outside a fence, a new bullet, a heading or any unindented line ends it. The
    bullet mark is not part of the first line.
    """
    found, current, fenced = [], None, False
    for line in text.splitlines():
        if CLAIM.match(line) and not (current and line.startswith(" ")):
            current = (BULLET_MARK.sub("", line.strip()), [])
            found.append(current)
            continue
        if line.strip().startswith("```"):
            fenced = not fenced
        keeps = fenced or (line.startswith(" ") and line.strip())
        if current and keeps and not BULLET.match(line):
            current[1].append(line.strip())
        elif not fenced:
            current = None
    return found


def changed_files(diff_text):
    """The file names the diff changes, in order, from the `+++ b/NAME` lines."""
    return re.findall(r"^\+\+\+ b/(\S+)", diff_text, re.M)


def test_names(text):
    """The names of the tests a file defines, in order."""
    return DEFINED.findall(text)


def has_pasted_output(rest):
    """True when a `$ command` line in rest is followed by a line of output.

    Blank lines and ``` fence lines between the command and the output are skipped.
    """
    for number, line in enumerate(rest):
        if PASTED.match(line):
            after = [l for l in rest[number + 1:] if l.strip() and l.strip() != "```"]
            if after and not PASTED.match(after[0]):
                return True
    return False


def judge(claim, defined):
    """(flagged, note) for one claim; defined is the list of test names in the diff."""
    first, rest = claim
    named = TEST_NAME.findall(" ".join([first, *rest]))
    missing = [name for name in dict.fromkeys(named) if name not in defined]
    if missing:
        return True, "no evidence: " + ", ".join(missing) + " is not defined in " \
            "the changed files"
    if named:
        return False, "evidence: " + ", ".join(dict.fromkeys(named)) + " is defined " \
            "in the changed files"
    if has_pasted_output(rest):
        command = next(line for line in rest if PASTED.match(line))
        return False, "evidence: output pasted under `" + command[2:] + "`"
    return True, "no evidence: no test name and no pasted command output"


def main(argv):
    if len(argv) != 1:
        print("usage: check_claims.py FOLDER_OR_PR_TEXT")
        return 2
    path = Path(argv[0])
    folder = path.parent if path.is_file() else path
    try:
        text = (folder / "pr_text.md").read_text(encoding="utf-8")
        diff = (folder / "diff.patch").read_text(encoding="utf-8")
        names = changed_files(diff)
        defined = []
        for name in names:
            defined += test_names((folder / name).read_text(encoding="utf-8"))
    except OSError as error:
        print(f"cannot read: {Path(error.filename or '?').name}")
        return 2
    found = claims(text)
    print(f"pr_text.md: {len(found)} claims")
    print(f"changed files (from diff.patch): {', '.join(names) or 'none'}")
    print(f"tests defined there: {', '.join(defined) or 'none'}")
    flagged = 0
    for number, claim in enumerate(found, 1):
        bad, note = judge(claim, defined)
        flagged += bad
        print(f"{number} {'FLAG' if bad else 'ok  '}  {claim[0]}")
        print(f"          {note}")
    print(f"{flagged} of {len(found)} claims flagged")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
