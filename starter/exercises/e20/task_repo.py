"""Shared pieces of exercise E20: a temporary git repository, worktrees, merges, tests.

Used by worktree_demo.py, not_a_sandbox.py and same_file_check.py. Needs git 2.5 or
newer (the first version with `git worktree`). Every git call runs with a fixed
identity, fixed dates and no user or system configuration, so the output of a run is
the same on every machine and never shows a path or a hash.
Interface for other code:
  require_git() exits with a message when git is missing or older than 2.5.
  git(ws, *args, check=True) runs git in folder ws and returns the CompletedProcess
      (text output). With check=True a non-zero exit raises RuntimeError.
  make_repo(root, files) makes root/main, a repository on branch main with one commit
      holding the files {name: text}, and returns its path.
  add_worktree(repo, name, detach=False) adds a worktree next to the repository, on a
      new branch called name (or on a detached HEAD at main), and returns its path.
  commit_all(ws, message) commits every change in ws.
  merge(ws, branch) merges branch into the HEAD of ws and returns [] when clean, or
      the list of files in conflict (the merge is left open). A merge that fails for
      another reason raises RuntimeError.
  run_tests(ws) runs unittest discovery in ws and returns (tests run, failed).
Failure modes: RuntimeError with the git message; SystemExit from require_git().
Standard library only.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

BANNER = "SCRIPTED DEMONSTRATION by the course authors, not a measurement"
MIN_GIT = (2, 5)
DATE = "2026-01-01T00:00:00+0000"
SECONDS = 30
GIT = ("git", "-c", "user.name=worktrees", "-c", "user.email=worktrees@example.invalid",
       "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false")
GIT_ENV = {**{k: v for k, v in os.environ.items() if not k.startswith("GIT_")},
           "GIT_AUTHOR_DATE": DATE, "GIT_COMMITTER_DATE": DATE,
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
           "HOME": os.devnull, "XDG_CONFIG_HOME": os.devnull,
           "PYTHONDONTWRITEBYTECODE": "1"}
RUNNER = """
import io, unittest
result = unittest.TextTestRunner(stream=io.StringIO()).run(
    unittest.defaultTestLoader.discover("."))
print(result.testsRun, len(result.failures) + len(result.errors))
"""

NAMES_BASE = {
    "names.py": '''def initials(name):
    """Upper-case first letters of the words in name: 'ada lovelace' gives 'AL'."""
    raise NotImplementedError
''',
    "test_names.py": '''import unittest

from names import initials


class TestInitials(unittest.TestCase):
    def test_two_words(self):
        self.assertEqual(initials("Ada Lovelace"), "AL")

    def test_lower_case_input(self):
        self.assertEqual(initials("grace brewster hopper"), "GBH")

    def test_extra_spaces(self):
        self.assertEqual(initials("  ada   lovelace "), "AL")

    def test_empty(self):
        self.assertEqual(initials(""), "")
''',
}

SHOP_BASE = {
    "prices.py": '''"""Prices in cents."""
PRICES = {"pen": 120, "book": 950}


def price(item):
    return PRICES[item]


def total(items):
    return sum(price(item) for item in items)
''',
    "test_prices.py": '''import unittest

from prices import price, total


class TestPrices(unittest.TestCase):
    def test_price(self):
        self.assertEqual(price("pen"), 120)

    def test_total(self):
        self.assertEqual(total(["pen", "book"]), 1070)
''',
}

SANDBOX_BASE = {"notes.txt": "notes for the agent\n", "config.txt": "mode = safe\n"}


def require_git():
    """Exit with a clear message unless `git --version` reports 2.5 or newer."""
    try:
        text = subprocess.run(["git", "--version"], capture_output=True,
                              text=True).stdout
    except OSError:
        text = ""
    found = re.search(r"(\d+)\.(\d+)", text)
    if not found:
        sys.exit("this exercise needs git; python3 check_env.py shows what you have")
    if (int(found[1]), int(found[2])) < MIN_GIT:
        sys.exit("this exercise needs git 2.5 or newer (git worktree); found "
                 + text.strip())


def git(ws, *args, check=True):
    """Run git in ws with the fixed identity and dates. See the module docstring."""
    done = subprocess.run([*GIT, *args], cwd=ws, env=GIT_ENV, capture_output=True,
                          text=True)
    if check and done.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {done.stderr.strip()}")
    return done


def commit_all(ws, message):
    git(ws, "add", "-A")
    git(ws, "commit", "-q", "-m", message)


def make_repo(root, files):
    """Make root/main on branch main with one commit holding files. Returns its path."""
    repo = Path(root) / "main"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "symbolic-ref", "HEAD", "refs/heads/main")  # not `init -b`: git < 2.28
    for name, text in files.items():
        (repo / name).write_text(text, encoding="utf-8")
    commit_all(repo, "base")
    return repo


def add_worktree(repo, name, detach=False):
    """Add the worktree root/name beside repo. Returns its path."""
    path = repo.parent / name
    if detach:
        git(repo, "worktree", "add", "--detach", str(path), "main")
    else:
        git(repo, "worktree", "add", "-b", name, str(path), "main")
    return path


def merge(ws, branch):
    """Merge branch into HEAD of ws. Returns [] when clean, else the conflict files."""
    done = git(ws, "merge", "--no-ff", "--no-edit", branch, check=False)
    if done.returncode == 0:
        return []
    conflicts = git(ws, "diff", "--name-only", "--diff-filter=U").stdout.split()
    if not conflicts:
        raise RuntimeError(f"git merge {branch} failed: {done.stderr.strip()}")
    return sorted(conflicts)


def run_tests(ws):
    """Run unittest discovery in ws. Returns (tests run, tests failed or errored)."""
    done = subprocess.run([sys.executable, "-B", "-c", RUNNER], cwd=ws,
                          capture_output=True, text=True, timeout=SECONDS,
                          env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    numbers = done.stdout.split()[-2:]
    if len(numbers) != 2 or not all(n.isdigit() for n in numbers):
        raise RuntimeError("the test runner printed no counts: " + done.stderr[-200:])
    return int(numbers[0]), int(numbers[1])
