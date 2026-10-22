"""Planner, three workers and a judge, one round, for exercise E19 (scripted).

Usage: python3 exercises/e19/team.py [--plan FILE] [--skip a,b] [--rogue b] [--dir DIR]
Copies the order package (shop/) into a temporary folder, then:
  1. the planner splits the task into three slices and writes ownership.json
     (or, with --plan FILE, that plan file is used and the planner does not run);
  2. a plan in which two owners claim one path is reported as a CONFLICT and no worker
     starts;
  3. each worker finishes its own slice and returns edits and one handoff line. The
     driver applies an edit only to a path its slice owns and REFUSES every other write;
  4. the judge runs the tests of each slice and decides CONTINUE or STOP.
--skip names workers that do not run (our script of a worker that never reported).
--rogue names a worker that also asks to change the shared interface file.
--dir DIR keeps the work folder (it must not exist yet); otherwise it is deleted.
Everything is a fixed script, offline, with no model. It shows the shape of the
pattern, not how a real planner or judge behaves.
Exit code: 0 when the judge says STOP with every test green, 1 for any other result,
2 for a bad option or plan file.
Interface for other code: apply_edit(root, plan, name, path, text) writes the edit
and returns None, or returns the reason it was refused and writes nothing;
refusal(plan, name, path) returns that reason or None. Standard library only.
"""
import sys

sys.dont_write_bytecode = True
import argparse  # noqa: E402
import hashlib  # noqa: E402
import shutil  # noqa: E402
import tempfile  # noqa: E402
import textwrap  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import judge  # noqa: E402
import planner  # noqa: E402
import worker  # noqa: E402

BANNER = "SCRIPTED DEMONSTRATION by the course authors, not a measurement"


def refusal(plan, name, path):
    """Why worker name may not write path, or None when its slice owns the path."""
    if path in plan["slices"][name]["owns"]:
        return None
    if path in plan["planner_only"]:
        return "planner only"
    owner = [n for n, body in plan["slices"].items() if path in body["owns"]]
    return f"owned by slice {owner[0]}" if owner else "not in its slice"


def apply_edit(root, plan, name, path, text):
    """Write text to root/path if slice name owns it. Returns None or the reason."""
    target = (Path(root) / path).resolve()
    reason = refusal(plan, name, path)
    if reason:
        return reason
    if Path(root).resolve() not in target.parents:
        return "outside the work folder"
    target.write_text(text, encoding="utf-8")
    return None


def snapshot(root):
    """{relative path: sha256} of every file under root/shop."""
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(Path(root, "shop").rglob("*")) if p.is_file()}


def show_conflicts(found):
    for path, owners in found:
        print(f"CONFLICT: {path} is claimed by {' and '.join(owners)}")


def run_workers(root, plan, skip, rogue):
    """Run each worker in turn. Returns its handoff lines."""
    print("\nworkers (a worker may write only the files its slice owns):")
    handoffs = []
    for name, body in plan["slices"].items():
        if name in skip:
            print(f"  {name}  did not run (our script of a worker that never reported)")
            continue
        edits, handoff = worker.work(name, body, root, rogue == name)
        handoffs.append(handoff)
        if not edits:
            print(f"  {name}  nothing to write")
        for path, text in edits:
            before = len(Path(root, path).read_text(encoding="utf-8").splitlines())
            reason = apply_edit(root, plan, name, path, text)
            if reason:
                print(f"  {name}  REFUSED {path}: {reason}")
            else:
                added = len(text.splitlines()) - before
                print(f"  {name}  wrote {path}, {added} lines added")
    return handoffs


def run_round(root, args):
    """One round in the prepared folder root. Returns the exit code."""
    shutil.copytree(HERE / "shop", Path(root) / "shop",
                    ignore=shutil.ignore_patterns("__pycache__"))
    start = snapshot(root)
    if args.plan:
        text = Path(args.plan).read_text(encoding="utf-8")
        (Path(root) / "ownership.json").write_text(text, encoding="utf-8")
        print(f"\nplan: {Path(args.plan).name} (read from a file, the planner did not "
              "run)")
        plan = planner.load_plan(Path(root) / "ownership.json")
    else:
        plan = planner.plan()
        path = planner.write_plan(root, plan)
        print("\nplanner: split the task into 3 slices and wrote ownership.json:")
        text = path.read_text(encoding="utf-8")
    print(text, end="")
    found = planner.conflicts(plan)
    if found:
        show_conflicts(found)
        decision, reason = judge.decide(plan, found, None)
        print("\n" + judge.verdict(decision, reason))
        return 1
    handoffs = run_workers(root, plan, args.skip, args.rogue)
    Path(root, "handoff.md").write_text("\n".join(handoffs) + "\n", encoding="utf-8")
    print("\nhandoff.md, one line per worker:")
    for line in handoffs:
        print(textwrap.fill(line, width=88, initial_indent="  ",
                            subsequent_indent="    "))
    results = judge.run_tests(root, plan)
    print("\njudge: ran the test class of each slice")
    print("  slice  tests        ran  failed")
    for name, (ran, bad) in results.items():
        print(f"  {name:<6} {plan['slices'][name]['tests']:<11} {ran:>4} {bad:>7}")
    decision, reason = judge.decide(plan, found, results)
    end = snapshot(root)
    changed = [p for p in end if start.get(p) != end[p]]
    print(f"\nfiles changed: {', '.join(changed) if changed else 'none'}")
    print(f"planner-only files unchanged: "
          f"{all(end.get(p) == start.get(p) for p in plan['planner_only'])}")
    print("\n" + judge.verdict(decision, reason))
    return 0 if decision == "STOP" else 1


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--plan", help="use this plan file, skip the planner")
    parser.add_argument("--skip", default="", help="workers that do not run, e.g. c")
    parser.add_argument("--rogue", help="a worker that also asks to change the "
                        "interface")
    parser.add_argument("--dir", help="keep the work folder here")
    args = parser.parse_args(argv)
    args.skip = [n for n in args.skip.split(",") if n]
    known = ("a", "b", "c")
    if args.plan and not Path(args.plan).is_file():
        parser.error(f"no such plan file: {args.plan}")
    if any(n not in known for n in args.skip + [args.rogue or "a"]):
        parser.error("--skip and --rogue take the slice names a, b and c")
    if args.dir and Path(args.dir).exists():
        parser.error(f"{args.dir} exists already; give a folder that does not exist")
    print(BANNER)
    print("team: one planner, three workers, one judge, one round. Scripted, offline.")
    try:
        if args.dir:
            Path(args.dir).mkdir(parents=True)
            return run_round(Path(args.dir), args)
        with tempfile.TemporaryDirectory(prefix="team_") as root:
            return run_round(Path(root), args)
    except ValueError as error:
        print(f"team: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
