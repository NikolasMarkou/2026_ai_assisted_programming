"""The scripted judge for exercise E19: run the tests, then continue or stop.

Usage: python3 exercises/e19/judge.py [WORKDIR]
Without WORKDIR the judge looks at a copy of the package as handed out, where every
slice is still a stub, and says CONTINUE. With WORKDIR (a folder holding shop/ and
ownership.json, for example one kept by team.py --dir) it judges that folder.
The judge reads no code and gives no opinion. It runs the test class of each slice
with the standard unittest module and decides from the counts:
  STOP      when the plan has an ownership conflict (nothing is run), or when every
            slice ran at least one test and none failed.
  CONTINUE  when a slice has a failing test or ran none: the reason names the slices.
Exit code: 0 for STOP with all tests green, 1 for any other decision.
Interface for other code: run_tests(root, plan) returns {slice: (ran, failed)};
decide(plan, found, results) returns (decision, reason) where found is the list from
planner.conflicts and results is the dict from run_tests or None when nothing was
run; verdict(decision, reason) returns the printed line. Standard library only.
"""
import sys

sys.dont_write_bytecode = True
import os  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
import textwrap  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import planner  # noqa: E402


def run_tests(root, plan):
    """Run the test class of each slice in root. Returns {slice: (ran, failed)}."""
    results = {}
    for name, body in plan["slices"].items():
        done = subprocess.run(
            [sys.executable, "-B", "-m", "unittest", f"shop.test_shop.{body['tests']}"],
            cwd=root, capture_output=True, text=True, timeout=60,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        ran = re.search(r"Ran (\d+) tests?", done.stderr)
        bad = sum(int(n) for n in re.findall(r"(?:failures|errors)=(\d+)", done.stderr))
        bad = bad or int(done.returncode != 0)
        results[name] = (int(ran[1]) if ran else 0, bad)
    return results


def decide(plan, found, results):
    """(decision, reason). decision is "STOP" or "CONTINUE"."""
    if found:
        paths = ", ".join(path for path, _ in found)
        word = "conflict" if len(found) == 1 else "conflicts"
        return ("STOP", f"The plan has {len(found)} ownership {word} ({paths}). "
                "No worker was started and no test was run. Split the task again "
                "before any worker starts.")
    open_slices = [n for n, (ran, bad) in results.items() if bad or not ran]
    if open_slices:
        names = ", ".join(open_slices)
        return ("CONTINUE", f"Tests are failing or missing for slice {names}. "
                "A next round would plan those slices again.")
    count = sum(ran for ran, _ in results.values())
    return ("STOP", f"All {count} tests pass in {len(results)} slices. "
            "Nothing is left to do.")


def verdict(decision, reason):
    """The decision line, wrapped to 88 columns."""
    return textwrap.fill(f"judge decision: {decision}. {reason}", width=88)


def main(argv):
    if len(argv) > 1:
        print("Usage: python3 exercises/e19/judge.py [WORKDIR]", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory(prefix="judge_") as scratch:
        root = Path(argv[0]) if argv else Path(scratch)
        if not argv:
            shutil.copytree(HERE / "shop", root / "shop",
                            ignore=shutil.ignore_patterns("__pycache__"))
        plan = (planner.load_plan(root / "ownership.json")
                if (root / "ownership.json").is_file() else planner.plan())
        found = planner.conflicts(plan)
        results = None if found else run_tests(root, plan)
        decision, reason = decide(plan, found, results)
    for name, (ran, bad) in (results or {}).items():
        print(f"slice {name}  {plan['slices'][name]['tests']:<11} ran {ran}, "
              f"failed {bad}")
    print(verdict(decision, reason))
    return 0 if decision == "STOP" and results else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
