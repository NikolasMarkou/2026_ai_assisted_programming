"""A worktree is not a sandbox: our own run with one scripted agent.

Usage: python3 exercises/e20/not_a_sandbox.py
The script makes a temporary repository (the main checkout) and one worktree on the
branch agent-a. The scripted agent works in the worktree, as it is told, and also
writes into the main checkout by its absolute path. Then a branch is made from the
worktree and read from the main checkout. Nothing here shows what any vendor tool
does: it shows what git does. The repository is deleted at the end; output has no
path and no hash. Needs git 2.5 or newer and a POSIX shell. Standard library only.
"""
import sys
import tempfile

import agents
from task_repo import (BANNER, SANDBOX_BASE, add_worktree, commit_all, git, make_repo,
                       require_git)


def status(ws):
    """Lines of `git status --short` in ws, indented; 'clean' when there are none."""
    lines = git(ws, "status", "--short").stdout.splitlines()
    return ["    " + line for line in lines] or ["    clean"]


def branches(ws):
    return git(ws, "for-each-ref", "--format=%(refname:short)",
               "refs/heads").stdout.split()


def main():
    require_git()
    print(BANNER)
    print("OUR OWN RUN: one scripted agent and one temporary repository."
          " No vendor tool is involved.\n")
    with tempfile.TemporaryDirectory(prefix="e20_") as root:
        main_checkout = make_repo(root, SANDBOX_BASE)
        work = add_worktree(main_checkout, "agent-a")
        print("setup: a main checkout with 1 commit and one worktree on branch agent-a")
        print("the agent runs in its worktree and is told to edit notes.txt there\n")
        print("PART 1. The agent writes outside its worktree")
        print("  main checkout before:")
        print("\n".join(status(main_checkout)))
        for command in agents.leaky_agent(work, main_checkout):
            print(f"  agent runs: {command}")
        print("  worktree agent-a after:")
        print("\n".join(status(work)))
        print("  main checkout after:")
        print("\n".join(status(main_checkout)))
        print("  Nothing stopped the two writes into the main checkout. A worktree is a"
              " separate")
        print("  folder of files. It does not limit where the agent can write.\n")
        print("PART 2. A branch made in one worktree is visible from another")
        git(work, "checkout", "-q", "-b", "from-a")
        (work / "notes.txt").write_text("a note from worktree agent-a\n")
        commit_all(work, "made in worktree agent-a")
        print("  in worktree agent-a: git checkout -b from-a, then a commit")
        seen = ", ".join(branches(main_checkout))
        print(f"  branches seen from the main checkout: {seen}")
        subject = git(main_checkout, "log", "-1", "--format=%s",
                      "from-a").stdout.strip()
        print(f"  last commit on from-a, read from the main checkout: {subject}")
        shared = (git(work, "rev-parse", "--git-common-dir").stdout.strip(),
                  git(main_checkout, "rev-parse", "--git-common-dir").stdout.strip())
        same = (work / shared[0]).resolve() == (main_checkout / shared[1]).resolve()
        print("  both folders use the same .git directory: "
              + ("yes\n" if same else "NO\n"))
    print("A worktree gives each agent its own files and its own checked-out branch.")
    print("It does not stop the agent writing to other paths, and the branches and"
          " history are shared.")
    print("Keeping an agent inside a folder is the job of the sandbox, one of the 4"
          " parts of an agent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
