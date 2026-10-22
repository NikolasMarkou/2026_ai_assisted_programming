"""The scripted planner for exercise E19: split the task, write ownership.json.

Usage: python3 exercises/e19/planner.py WORKDIR
Writes WORKDIR/ownership.json for the order package in WORKDIR/shop: three slices,
each with the one file its worker owns and the test class that judges it, and a list
of planner-only files that no worker may write. The split is a fixed script, not a
model: it shows what a plan has to contain, not how a real planner decides.
Interface for other code: SLICES is the split; plan() returns it as a dict with the
keys "planner_only" (list of paths) and "slices" ({name: {"goal", "owns", "tests"}});
write_plan(root, plan) writes ownership.json in the two-lines-per-slice layout that
overlap.json uses and returns its path; conflicts(plan) returns [(path, [slice names
or "planner only"])] for every path that two owners claim, sorted, empty when the plan
is sound; load_plan(path) reads a plan file and raises ValueError when it is not
shaped like one. Standard library only.
"""
import sys

sys.dont_write_bytecode = True
import json  # noqa: E402
from pathlib import Path  # noqa: E402

PLANNER_ONLY = ["shop/interface.py", "shop/test_shop.py"]
SLICES = {
    "a": ("read an order from text", "shop/parse.py", "TestParse"),
    "b": ("compute the total with the discount", "shop/total.py", "TestTotal"),
    "c": ("render the receipt text", "shop/render.py", "TestRender"),
}


def plan():
    """The split: every slice owns one file, the interface and tests are frozen."""
    return {"planner_only": list(PLANNER_ONLY),
            "slices": {name: {"goal": goal, "owns": [path], "tests": tests}
                       for name, (goal, path, tests) in SLICES.items()}}


def render_plan(data):
    """The text of a plan file: two lines per slice, as in overlap.json."""
    rows = [f"    {json.dumps(name)}: {{\"owns\": {json.dumps(body['owns'])}, "
            f"\"tests\": {json.dumps(body['tests'])},\n"
            f"          \"goal\": {json.dumps(body['goal'])}}}"
            for name, body in data["slices"].items()]
    return ("{\n  \"planner_only\": " + json.dumps(data["planner_only"]) + ",\n"
            "  \"slices\": {\n" + ",\n".join(rows) + "\n  }\n}\n")


def write_plan(root, data):
    """Write ownership.json in the folder root. Returns its path."""
    path = Path(root) / "ownership.json"
    path.write_text(render_plan(data), encoding="utf-8")
    return path


def conflicts(data):
    """Paths claimed by two owners, as [(path, owners)]; empty when the plan is sound.

    A path claimed by two slices is a conflict, and so is a slice that claims a
    planner-only path.
    """
    owners = {}
    for path in data["planner_only"]:
        owners.setdefault(path, []).append("planner only")
    for name, body in data["slices"].items():
        for path in body["owns"]:
            owners.setdefault(path, []).append(name)
    return sorted((path, who) for path, who in owners.items() if len(who) > 1)


def load_plan(path):
    """Read a plan file. Raises ValueError (with the reason) when it is malformed."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read {path}: {error}") from error
    slices = data.get("slices") if isinstance(data, dict) else None
    ok = (isinstance(slices, dict) and slices
          and isinstance(data.get("planner_only"), list)
          and all(isinstance(b, dict) and isinstance(b.get("owns"), list)
                  and isinstance(b.get("tests"), str) and isinstance(b.get("goal"), str)
                  for b in slices.values()))
    if not ok:
        raise ValueError(f"{path} is not a plan: it needs planner_only and slices, "
                         "each slice with goal, owns and tests")
    return data


def main(argv):
    if len(argv) != 1:
        print("Usage: python3 exercises/e19/planner.py WORKDIR", file=sys.stderr)
        return 2
    root = Path(argv[0])
    root.mkdir(parents=True, exist_ok=True)
    print(f"planner: wrote {write_plan(root, plan()).name} in {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
