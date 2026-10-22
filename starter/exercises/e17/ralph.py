"""Ralph loop driver for exercise E17: a new context every pass, state in files.

Usage: python3 exercises/e17/ralph.py [--max-iterations N] [--dir DIR] [--once]
           [--live]
Each pass reads PROMPT.md, runs minimal_agent.agent() once with a new message list,
and appends one line to progress.md. The loop stops when fix_plan.md has no unchecked
item (exit 0), or after N passes with an item still open (exit 1 and a STOP line).
N is 5 unless you set it. 0, a negative number and "no limit" are refused: the loop is
never unlimited. Without --dir the work happens in a temporary copy of this folder
that is deleted at the end. With --dir DIR the copy is made there when DIR does not
exist yet, and it is kept; an existing DIR is used as it is, so pass numbers go on.
--once runs one pass in DIR and returns: ralph.sh calls it in a shell loop.
--live calls the real Messages API instead of item_model.py: it needs
ANTHROPIC_API_KEY, costs money, and gives a real model a shell with no sandbox. A key
in the environment never switches it on. The default model is scripted and offline.
Interface for other code: prepare(ws) copies the four exercise files into the new
folder ws and commits them; open_items(ws) returns the unchecked lines of
ws/fix_plan.md; run_loop(ws, model, cap) returns ("done" or "cap", rows) with one
row (pass, context items sent, open before, open after) per pass.
Standard library only.
"""
import sys

sys.dont_write_bytecode = True
import argparse  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent.parent / "agent"), str(HERE)]
import item_model  # noqa: E402
import minimal_agent  # noqa: E402

BANNER = "SCRIPTED DEMONSTRATION by the course authors, not a measurement"
FILES = ("PROMPT.md", "fix_plan.md", "items.py", "test_items.py")
CAP = 5
DATE = "2026-01-01T00:00:00+0000"
GIT = ("git", "-c", "user.name=ralph", "-c", "user.email=ralph@example.invalid",
       "-c", "commit.gpgsign=false")
GIT_ENV = {"GIT_AUTHOR_DATE": DATE, "GIT_COMMITTER_DATE": DATE,
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}
# The agent's shell commits in the work folder: give it the same fixed settings.
for _name in [n for n in minimal_agent.ENV if n.startswith("GIT_")]:
    del minimal_agent.ENV[_name]
minimal_agent.ENV.update(GIT_ENV)


def prepare(ws):
    """Make the new folder ws a git repository holding the four exercise files."""
    ws.mkdir(parents=True)
    for name in FILES:
        shutil.copy(HERE / name, ws / name)
    env = {**minimal_agent.ENV, **GIT_ENV}
    for args in (("init", "-q"), ("add", "-A"), ("commit", "-q", "-m", "base")):
        subprocess.run([*GIT, *args], cwd=ws, env=env, check=True,
                       capture_output=True)


def open_items(ws):
    """The unchecked item lines of ws/fix_plan.md."""
    return re.findall(r"^- \[ \] .*$", (ws / "fix_plan.md").read_text(encoding="utf-8"),
                      re.M)


def recording(model, said):
    """Wrap model so that said[:] holds the last text block it returned."""
    def call(messages):
        reply = model(messages)
        said[:] = [b["text"] for b in reply["content"] if b["type"] == "text"][-1:]
        return reply
    return call


def first_sentence(said):
    """The first sentence of the agent's last text, for the progress line."""
    return " ".join(said).split(". ")[0].strip().rstrip(".") + "."


def one_pass(ws, model):
    """One pass: the prompt is read again and the agent starts with a new message list.

    Appends a line to ws/progress.md. Returns (pass number, context items sent in the
    last request, open items before, open items after). The pass number is the number
    of lines in progress.md plus 1, so it is kept in a file and not in this process.
    """
    log = ws / "progress.md"
    number = (len(log.read_text().splitlines()) if log.exists() else 0) + 1
    before, said = len(open_items(ws)), []
    print(f"\npass {number}: new context, PROMPT.md is read again")
    task = (ws / "PROMPT.md").read_text(encoding="utf-8")
    sent = minimal_agent.agent(task, ws, recording(model, said))
    after = len(open_items(ws))
    print(f"  open items {before} -> {after}, context items sent in the last "
          f"request {sent}")
    with log.open("a", encoding="utf-8") as handle:
        handle.write(f"pass {number} | open items {before} -> {after} | context "
                     f"items sent {sent} | {first_sentence(said)}\n")
    return number, sent, before, after


def run_loop(ws, model, cap):
    """Run passes until nothing is open or cap passes have run. Prints each pass.

    Returns ("done" or "cap", rows). "cap" means the cap stopped the loop while at
    least one item was still open. cap must be 1 or more; main() refuses less.
    """
    rows = []
    for _ in range(cap):
        if not open_items(ws):
            break
        rows.append(one_pass(ws, model))
    return ("cap" if open_items(ws) else "done"), rows


def show_state(ws):
    """Print fix_plan.md, progress.md and the git log subjects of ws."""
    print("\nfix_plan.md now:")
    for line in (ws / "fix_plan.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("- ["):
            print(f"  {line}")
    print("progress.md:")
    for line in (ws / "progress.md").read_text(encoding="utf-8").splitlines():
        print(f"  {line}")
    log = subprocess.run([*GIT, "log", "--reverse", "--format=%s"], cwd=ws,
                         env={**minimal_agent.ENV, **GIT_ENV}, capture_output=True,
                         text=True).stdout
    print("git log, oldest first:")
    for subject in log.splitlines():
        print(f"  {subject}")


def drive(ws, args):
    """Run what args asks for in ws. Returns the exit code."""
    if not ws.exists():
        prepare(ws)
    model = minimal_agent.call_model if args.live else item_model.call_model
    if args.once:
        one_pass(ws, model)
        return 0
    status, rows = run_loop(ws, model, args.max_iterations)
    show_state(ws)
    left = open_items(ws)
    if status == "done":
        word = "pass" if len(rows) == 1 else "passes"
        print(f"\nDONE: no open item after {len(rows)} {word}. The loop stopped "
              "itself.")
        return 0
    ids = ", ".join(re.match(r"- \[ \] (\d+)", line)[1] for line in left)
    print(f"\nSTOP: --max-iterations {args.max_iterations} reached with {len(left)} "
          f"open item(s): {ids}. No further pass will run.")
    print("The state is in fix_plan.md, progress.md and git. A person decides next.")
    return 1


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--max-iterations", type=int, default=CAP, metavar="N")
    parser.add_argument("--dir", help="work here and keep the folder")
    parser.add_argument("--once", action="store_true",
                        help="run one pass (needs --dir)")
    parser.add_argument("--live", action="store_true", help="call the real API")
    args = parser.parse_args(argv)
    if args.max_iterations < 1:
        parser.error("--max-iterations must be 1 or more: this loop is never unlimited")
    if args.once and not args.dir:
        parser.error("--once needs --dir")
    if args.live and not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("--live needs ANTHROPIC_API_KEY in the environment")
    if args.live:
        print("warning: live run. The prompt goes to the API with your key, and the "
              "model runs shell commands in the work folder with no sandbox.")
    elif not args.once:
        print(BANNER)
    if not args.once:
        print(f"ralph: {'live model' if args.live else 'scripted model'}, "
              f"up to {args.max_iterations} passes, a new context each pass")
    if args.dir:
        return drive(Path(args.dir).resolve(), args)
    with tempfile.TemporaryDirectory(prefix="ralph_") as root:
        return drive(Path(root) / "work", args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
