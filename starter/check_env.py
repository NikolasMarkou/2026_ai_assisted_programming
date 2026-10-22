"""Check the machine before the exercises: Python 3.10+, git, and the agent tools.

Usage: python3 check_env.py
Prints one line per item. Exit code 1 when Python is older than 3.10 or git is missing.
A missing agent tool is not an error: the offline scripted agent needs none.
Standard library only.
"""
import shutil
import subprocess
import sys

MIN_PYTHON = (3, 10)
AGENT_TOOLS = ("claude", "codex", "cursor", "opencode")


def git_version() -> str | None:
    """The text of `git --version`, or None when git is missing or does not run."""
    if not shutil.which("git"):
        return None
    done = subprocess.run(["git", "--version"], capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 else None


def main() -> int:
    python_ok = sys.version_info[:2] >= MIN_PYTHON
    git = git_version()
    rows = [("python", "ok" if python_ok else "TOO OLD", sys.version.split()[0]),
            ("git", "ok" if git else "MISSING", git or "install git")]
    for tool in AGENT_TOOLS:
        path = shutil.which(tool)
        rows.append((tool, "found" if path else "not found", path or "-"))
    for name, status, detail in rows:
        print(f"{name:10} {status:10} {detail}")
    if not python_ok:
        print(f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or newer is required.")
    return 0 if python_ok and git else 1


if __name__ == "__main__":
    sys.exit(main())
