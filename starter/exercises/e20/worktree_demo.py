"""Two scripted agents in two git worktrees: best-of-N, then merge order.

Usage: python3 exercises/e20/worktree_demo.py best [--pick a|b] [--apply]
       python3 exercises/e20/worktree_demo.py merge
best: one task, solved by two agents, each in its own worktree. You look at both
  results and pick one with --pick (default a). Nothing is merged back: the pick stays
  on its branch and main does not move. --apply merges the pick yourself afterwards.
merge: three pairs of agents, each pair on two different tasks. For every pair the
  script runs same_file_check.py, then merges the two branches in a scratch worktree,
  agent-a first and then agent-b first, and runs the tests after every merge.
Every repository is created in a temporary folder and deleted at the end. Output has
no path and no hash. Needs git 2.5 or newer. Standard library only.
"""
import argparse
import sys
import tempfile

import agents
import same_file_check
from task_repo import (BANNER, NAMES_BASE, SHOP_BASE, add_worktree, commit_all, git,
                       make_repo, merge, require_git, run_tests)


def show_tests(counts):
    ran, failed = counts
    return f"{ran} ran, {failed} failed"


def run_agents(repo, team):
    """Create one worktree per agent, run the agent in it and commit its work."""
    for name, agent in team.items():
        ws = add_worktree(repo, name)
        commit_all(ws, f"{name}: {agent(ws)}")


def best_of_n(pick, apply):
    with tempfile.TemporaryDirectory(prefix="e20_") as root:
        repo = make_repo(root, NAMES_BASE)
        base = git(repo, "rev-parse", "main").stdout
        print("PART 1. Best-of-N: one task, two agents, two worktrees")
        print("task: write initials(name) in names.py; the tests are in test_names.py")
        print("repository: main has 1 commit and names.py is a stub")
        run_agents(repo, agents.BEST_OF_N)
        count = len(git(repo, "worktree", "list").stdout.splitlines())
        print(f"worktrees: {count} in all (the main checkout and 2), one branch each")
        again = git(repo, "worktree", "add", str(repo.parent / "again"), "agent-a",
                    check=False)
        print("a second worktree on branch agent-a: "
              + ("refused" if again.returncode else "allowed"))
        print("  (git checks a branch out in one worktree only, unless you force it)")
        print()
        for name in agents.BEST_OF_N:
            ws = repo.parent / name
            files = same_file_check.touched(repo, "main", name)
            handoff = git(repo, "log", "-1", "--format=%s", name).stdout.strip()
            print(f"{name}: files changed: {', '.join(files)}; "
                  f"tests: {show_tests(run_tests(ws))}")
            print(f"  handoff: {handoff.split(': ', 1)[1]}")
        winner = "agent-" + pick
        print()
        print(f"you pick: {winner} (from --pick, default a)")
        if apply:
            merge(repo, winner)
            print(f"--apply: you merged {winner} into main."
                  f" Tests in main: {show_tests(run_tests(repo))}")
        else:
            stub = "NotImplementedError" in (repo / "names.py").read_text()
            unmoved = git(repo, "rev-parse", "main").stdout == base
            clean = not git(repo, "status", "--short").stdout
            print("main after the pick:")
            print(f"  still at the base commit: {'yes' if unmoved else 'NO'}")
            print(f"  names.py is still the stub: {'yes' if stub else 'NO'}")
            print(f"  working tree clean: {'yes' if clean else 'NO'}")
            print("Nothing was merged back. To keep the pick you merge it yourself"
                  " (--apply).")


def merge_both_orders(repo, names):
    """Merge the two branches in a scratch worktree, once per order. Returns lines
    and the final trees (None for an order that stopped on a conflict)."""
    lines, trees = [], []
    for number, order in enumerate((names, names[::-1])):
        scratch = add_worktree(repo, f"scratch-{number}", detach=True)
        lines.append(f"  order {order[0]} then {order[1]}")
        tree = git(scratch, "rev-parse", "HEAD^{tree}").stdout
        for branch in order:
            conflicts = merge(scratch, branch)
            if conflicts:
                lines.append(f"    merge {branch}: CONFLICT in {', '.join(conflicts)},"
                             " tests: not run")
                tree = None
                break
            counts = run_tests(scratch)
            lines.append(f"    merge {branch}: clean, tests: {show_tests(counts)}")
            tree = git(scratch, "rev-parse", "HEAD^{tree}").stdout
        trees.append(tree)
    return lines, trees


def merge_order():
    print("PART 2. Two agents, two different tasks, one base: merge order")
    print("For each pair: the same-file check, then agent-a merged first and agent-b"
          " merged first.")
    print("Tests run after every merge.")
    for number, (title, team) in enumerate(agents.PAIRS, 1):
        with tempfile.TemporaryDirectory(prefix="e20_") as root:
            repo = make_repo(root, SHOP_BASE)
            run_agents(repo, team)
            print(f"\npair {number}: {title}")
            for name in team:
                handoff = git(repo, "log", "-1", "--format=%s", name).stdout.strip()
                print(f"  {name} did: {handoff.split(': ', 1)[1]}")
            by_branch = {name: same_file_check.touched(repo, "main", name)
                         for name in team}
            for line in same_file_check.report(by_branch):
                print("  " + line)
            lines, trees = merge_both_orders(repo, list(team))
            print("\n".join(lines))
            if all(trees):
                same = trees[0] == trees[1]
                print("  final files identical in both orders: "
                      + ("yes" if same else "no"))
    print("\nWhat to take from it:")
    print("- Git reports the conflict of pair 2 only at the merge. The same-file"
          " check reports")
    print("  the overlap before it.")
    print("- Pair 3 has no shared file and no conflict. Only the tests after the merge"
          " fail,")
    print("  and which merge turns them red depends on the order.")
    print("- Merge order is our own exercise. No vendor page documents a merge order"
          " or two agents")
    print("  editing one file.")


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("part", choices=("best", "merge"))
    parser.add_argument("--pick", choices=("a", "b"), default="a")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    require_git()
    print(BANNER)
    print("two scripted agents, temporary git repositories, no model runs\n")
    if args.part == "best":
        best_of_n(args.pick, args.apply)
    else:
        merge_order()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
