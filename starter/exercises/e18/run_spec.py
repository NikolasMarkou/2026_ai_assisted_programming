"""Run the E17 loop with the numbers from a loop spec (exercise E18), scripted.

Usage: python3 exercises/e18/run_spec.py SPEC.md
Reads SPEC.md and grades it with check_spec.py. A spec that fails is not run: the
reasons are printed and the exit code is 2. A spec that passes gives two things to
exercises/e17/ralph.py: the number of passes from the stopping rule, which becomes
--max-iterations, and the memory file from the memory field, which is read after the
run from the work folder of the loop. The script prints those two lines of the spec,
then the run of ralph.py (scripted model, offline, in a temporary folder that is
deleted at the end). The other three fields are shown and not acted on: the trigger is
this command, the goal is not evaluated here, and ralph.py runs the test of each item
itself, not the verification command of the spec.
Exit code: 0 when the loop finished all items, 1 when the cap stopped it with an item
open, 2 when the spec fails the check, ralph.py is missing, or the memory file named
in the spec was not written by the loop. It needs the folder layout of starter/
(agent/ and exercises/e17/ next to exercises/e18/).
Interface for other code: fields_used(text) returns (cap, memory file, body) for a
spec text that passed check_spec.check, where body is {field: one-line body}.
Standard library only.
"""
import sys

sys.dont_write_bytecode = True
import subprocess  # noqa: E402
import tempfile  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_spec  # noqa: E402

BANNER = "SCRIPTED DEMONSTRATION by the course authors, not a measurement"
RALPH = HERE.parent / "e17" / "ralph.py"
SHOWN = ("trigger", "goal", "verification")


def fields_used(text):
    """(cap, memory file, bodies) of a spec that passed check_spec.check."""
    body = check_spec.parse(text)
    return (check_spec.cap_of(body["stopping rule"]),
            check_spec.memory_file_of(body["memory"]), body)


def short(line, width=88):
    """A one-line body cut to width characters."""
    return line if len(line) <= width else line[:width - 3] + "..."


def memory_line(work, name):
    """Describe the memory file name in the work folder, or None when it is absent."""
    path = (work / name).resolve()
    if work.resolve() not in path.parents or not path.is_file():
        return None
    lines = path.read_text(encoding="utf-8").splitlines()
    last = short(lines[-1], 70) if lines else "(empty)"
    return f"{len(lines)} lines, last: {last}"


def main(argv):
    if len(argv) != 1:
        print("Usage: python3 exercises/e18/run_spec.py SPEC.md", file=sys.stderr)
        return 2
    spec = Path(argv[0])
    try:
        text = spec.read_text(encoding="utf-8")
    except OSError as error:
        print(f"run_spec: cannot read {spec}: {error.strerror}", file=sys.stderr)
        return 2
    result = check_spec.check(text)
    if any(result.values()):
        check_spec.report(spec.name, result)
        print("run_spec: the spec fails the check. Nothing was run.")
        return 2
    if not RALPH.is_file():
        print("run_spec: exercises/e17/ralph.py is missing. Use a full copy of "
              "starter/.", file=sys.stderr)
        return 2
    cap, memory, body = fields_used(text)
    print(BANNER)
    print(f"run_spec: {spec.name} passes check_spec, all 5 fields")
    print("used from the spec:")
    print(f"  stopping rule  cap {cap}, passed as --max-iterations {cap}")
    print(f"                 line: {short(body['stopping rule'])}")
    print(f"  memory         file {memory}, read from the work folder after the run")
    print(f"                 line: {short(body['memory'])}")
    print("shown, not acted on:")
    for field in SHOWN:
        print(f"  {field:<14} {short(body[field])}")
    with tempfile.TemporaryDirectory(prefix="run_spec_") as root:
        work = Path(root) / "work"
        ran = subprocess.run([sys.executable, str(RALPH), "--max-iterations", str(cap),
                              "--dir", str(work)], capture_output=True, text=True,
                             timeout=120)
        lines = ran.stdout.splitlines()
        print("\n".join(lines[1:] if lines[:1] == [BANNER] else lines))
        sys.stdout.write(ran.stderr)
        found = memory_line(work, memory)
    if found is None:
        print(f"\nSTOP: the spec names {memory} as its memory, but the loop wrote no "
              "file with that name in its work folder. The E17 loop keeps its state in "
              "progress.md and fix_plan.md.")
        return 2
    print(f"\nmemory file {memory} after the run: {found}")
    return ran.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
