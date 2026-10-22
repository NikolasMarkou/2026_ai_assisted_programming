"""Lint an AGENTS.md: instruction files go stale like any list of dependencies.

Usage: python3 lint_agents_md.py path/to/AGENTS.md
Checks every command and folder the file names against the repository around it,
that the file names a command that runs the tests, and that it is not too long.
Exit code 0 when nothing is wrong, 1 otherwise. Standard library only.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

MAX_LINES = 100  # a limit chosen for this exercise, not a vendor rule
KNOWN_TOOLS = ("uv", "make", "npm", "pytest", "python", "python3", "git", "node",
               "ruff", "mypy", "cargo", "go", "pip")


def command_exists(span: str, root: Path) -> bool:
    """True when the first word is installed and, for make, the target exists."""
    tool = span.split()[0]
    if not shutil.which(tool):
        return False
    if tool != "make":
        return True
    dry_run = span.replace("make", "make -n", 1)  # a target can be gone, make remains
    done = subprocess.run(dry_run, shell=True, cwd=root, capture_output=True)
    return done.returncode == 0


def lint(text: str, root: Path) -> list[tuple[str, str, str]]:
    """Check AGENTS.md text against the repository in directory root.

    Returns a list of (status, kind, detail) tuples. status is "ok", "GONE",
    "MISSING" or "TOO LONG"; kind is "command", "path", "tests" or "length".
    """
    findings = []
    commands = []
    for span in re.findall(r"`([^`]+)`", text):
        if span.endswith("/"):
            found = (Path(root) / span).is_dir()
            findings.append(("ok" if found else "GONE", "path", span))
        elif span.split() and span.split()[0] in KNOWN_TOOLS:
            commands.append(span)
            found = command_exists(span, root)
            findings.append(("ok" if found else "GONE", "command", span))
    if not any("test" in span for span in commands):
        findings.append(("MISSING", "tests", "no command that runs the tests"))
    lines = len(text.splitlines())
    if lines > MAX_LINES:
        findings.append(("TOO LONG", "length", f"{lines} lines, limit {MAX_LINES}"))
    return findings


def main(argv: list[str]) -> int:
    """Print one line per finding. Returns 0 if all are ok, 1 if not, 2 on bad usage."""
    if len(argv) != 1:
        print("Usage: python3 lint_agents_md.py path/to/AGENTS.md")
        return 2
    path = Path(argv[0])
    findings = lint(path.read_text(), path.resolve().parent)
    for status, kind, detail in findings:
        print(f"{status:8} {kind:8} {detail}")
    return 0 if all(status == "ok" for status, _, _ in findings) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
