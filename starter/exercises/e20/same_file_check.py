"""List the files each branch touched and flag a file that two branches touched.

Usage: python3 exercises/e20/same_file_check.py REPO BASE BRANCH BRANCH [BRANCH ...]
REPO is a git repository (a main checkout or any worktree of it), BASE the branch the
others started from, and each BRANCH one agent's branch. For every branch it prints the
files changed since the branch left BASE (`git diff --name-only BASE...BRANCH`). A file
that appears in two or more branches is flagged before anything is merged.
Exit code 0 when no file is in two branches, 1 when one is, 2 for a bad argument.
What the check cannot see: two branches that touch different files can still break each
other once merged (a renamed function that another branch calls). Only the tests run
on the merged result see that.
Interface for other code: touched(repo, base, branch) returns the sorted file list;
overlaps(by_branch) maps each file found in 2 or more branches to those branches;
report(by_branch) returns the lines this script prints.
Standard library only.
"""
import sys
from pathlib import Path

from task_repo import git, require_git


def touched(repo, base, branch):
    """Sorted files that BRANCH changed since it left BASE."""
    done = git(repo, "diff", "--name-only", f"{base}...{branch}")
    return sorted(done.stdout.split())


def overlaps(by_branch):
    """{file: [branches]} for every file that two or more branches touched."""
    owners = {}
    for branch, files in by_branch.items():
        for name in files:
            owners.setdefault(name, []).append(branch)
    return {name: who for name, who in sorted(owners.items()) if len(who) > 1}


def report(by_branch):
    """The lines of the report: one per branch, then the verdict."""
    lines = [f"{branch} touched: {', '.join(files) or 'no file'}"
             for branch, files in by_branch.items()]
    shared = overlaps(by_branch)
    if not shared:
        return lines + ["same-file check: no file is in two branches"]
    lines.append("same-file check: OVERLAP")
    return lines + [f"  {name} is in {' and '.join(who)}"
                    for name, who in shared.items()]


def main(argv):
    if len(argv) < 4:
        print("usage: same_file_check.py REPO BASE BRANCH BRANCH [BRANCH ...]")
        return 2
    require_git()
    repo, base, branches = Path(argv[0]), argv[1], argv[2:]
    try:
        by_branch = {branch: touched(repo, base, branch) for branch in branches}
    except (RuntimeError, OSError) as error:
        print(f"cannot read the branches: {error}")
        return 2
    print("\n".join(report(by_branch)))
    return 1 if overlaps(by_branch) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
