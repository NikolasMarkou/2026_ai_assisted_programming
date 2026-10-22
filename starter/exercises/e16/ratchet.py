"""Autoresearch ratchet for exercise E16, on a toy task, with scripted proposers.

Usage: python3 exercises/e16/ratchet.py [--proposer improve|edit_evaluator|hardcode]
           [--budget 6] [--rule-only] [--hidden PATH] [--out results.tsv]
The driver copies prepare.py, candidate.py and program.md into a temporary git
repository and records the sha256 of the two protected files. Then, for each of the
BUDGET proposals: the proposer returns new file texts; the driver rejects the
proposal when a protected file or any file other than candidate.py changed; otherwise
it commits, runs `python3 prepare.py` in the repository and reads the `score:` line.
The commit stays only if the visible score is strictly better than the best so far;
otherwise the driver resets to the previous commit. It writes results.tsv and prints
the git log, which holds the kept proposals only. The repository is deleted at the end.
--rule-only turns the protected-file check off: only the rule in program.md is left.
--hidden PATH scores the first and the final candidate on the trainer's hidden cases.
Identity and dates of every commit are fixed, so the output is the same on every run.
Interface for other code: run_loop(ws, propose, budget, rule_only) returns
(start score, table rows); evaluate(ws) returns ((passed, total) or None, log text).
Standard library only.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent.parent / "evals"), str(HERE.parent.parent / "agent")]
import harness  # noqa: E402  (touched() lists the paths a proposal changed)
import proposers  # noqa: E402
from minimal_agent import ENV as RUN_ENV  # noqa: E402  (no KEY, TOKEN, SECRET vars)

BANNER = "SCRIPTED DEMONSTRATION by the course authors, not a measurement"
FILES = ("prepare.py", "candidate.py", "program.md")
PROTECTED = ("prepare.py", "program.md")
MUTABLE = "candidate.py"
BUDGET = 6
SECONDS = 30
DATE = "2026-01-01T00:00:00+0000"
GIT = ("git", "-c", "user.name=ratchet", "-c", "user.email=ratchet@example.invalid",
       "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false")
GIT_ENV = {**{k: v for k, v in os.environ.items() if not k.startswith("GIT_")},
           "GIT_AUTHOR_DATE": DATE, "GIT_COMMITTER_DATE": DATE,
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
           "PYTHONDONTWRITEBYTECODE": "1"}
HIDDEN_RUNNER = """
import importlib.util, sys
sys.path.insert(0, sys.argv[1])
import prepare
spec = importlib.util.spec_from_file_location("hidden_set", sys.argv[3])
hidden = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hidden)
print(*prepare.grade(prepare.load_function(sys.argv[2]), hidden.HIDDEN))
"""


def git(ws, *args):
    """Run git in ws with the fixed identity and dates; returns stdout."""
    done = subprocess.run([*GIT, *args], cwd=ws, env=GIT_ENV, capture_output=True,
                          text=True, check=True)
    return done.stdout


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def start_repo(ws):
    """Make ws a new repository holding the three exercise files in one commit."""
    ws.mkdir()
    for name in FILES:
        shutil.copy(HERE / name, ws / name)
    git(ws, "init", "-q")
    git(ws, "add", "-A")
    git(ws, "commit", "-q", "-m", "base")


def evaluate(ws):
    """Run prepare.py in ws, the way an agent runs it. Returns (score, log).

    score is (passed, total) read from the last `score: N/M` line, or None when the
    run printed no such line or took longer than SECONDS (a crash).
    """
    try:
        done = subprocess.run([sys.executable, "-B", "prepare.py"], cwd=ws,
                              env=RUN_ENV, capture_output=True, text=True,
                              timeout=SECONDS)
    except subprocess.TimeoutExpired:
        return None, f"timed out after {SECONDS} seconds\n"
    log = done.stdout + done.stderr
    found = re.findall(r"^score: (\d+)/(\d+)$", log, re.M)
    return ((int(found[-1][0]), int(found[-1][1])) if found else None), log


def violations(ws, recorded, changed):
    """Reasons to reject a proposal. An empty list means only candidate.py changed."""
    reasons = [f"{name} no longer matches its recorded sha256" for name, old
               in recorded.items() if not (ws / name).exists()
               or digest(ws / name) != old]
    reasons += [f"{path} is not the mutable file" for path in changed
                if path != MUTABLE and path not in recorded]
    return reasons


def inside(name):
    """True when name stays inside the repository."""
    return not Path(name).is_absolute() and ".." not in Path(name).parts


def run_loop(ws, propose, budget, rule_only):
    """Run the ratchet in repository ws. Prints each proposal.

    Returns (start score, rows). A row is (number, score text or '-', status,
    description); status is keep, discard, crash or rejected. Failure mode: exits when
    the starting candidate prints no score; ValueError from a proposer whose script no
    longer matches the files.
    """
    recorded = {name: digest(ws / name) for name in PROTECTED}
    print("protected files: " + ", ".join(
        f"{name} sha256 {code[:10]}" for name, code in recorded.items()))
    start, _ = evaluate(ws)
    if start is None:
        sys.exit("the starting candidate printed no score line")
    best = start
    print(f"start: visible score {start[0]}/{start[1]}")
    rows = []
    for number in range(1, budget + 1):
        files = {name: (ws / name).read_text() for name in FILES}
        made = propose(number, files)
        if made is None:
            print(f"\nthe proposer has no more ideas after {number - 1} of "
                  f"{budget} proposals")
            break
        description, changes = made
        print(f"\nproposal {number}: {description}")
        head = git(ws, "rev-parse", "HEAD").strip()
        for name, text in changes.items():
            if inside(name):
                (ws / name).write_text(text)
        changed = harness.touched(ws, head) + [n for n in changes if not inside(n)]
        print(f"  changed: {', '.join(changed) or 'nothing'}")
        why = violations(ws, recorded, changed)
        if why and not rule_only:
            git(ws, "reset", "-q", "--hard", head)
            git(ws, "clean", "-q", "-fdx")
            print(f"  REJECTED: {why[0]}; the files are restored")
            rows.append((number, "-", "rejected", description))
            continue
        git(ws, "add", "-A")
        git(ws, "commit", "-q", "--allow-empty", "-m", f"proposal {number}: "
            f"{description}")
        score, _ = evaluate(ws)
        text = f"{score[0]}/{score[1]}" if score else "-"
        if score and score[0] > best[0]:
            print(f"  visible {text}, best so far {best[0]}/{best[1]}: keep")
            best, status = score, "keep"
        else:
            status = "discard" if score else "crash"
            print(f"  visible {text}, best so far {best[0]}/{best[1]}: {status}, "
                  "reset to the previous commit")
            git(ws, "reset", "-q", "--hard", "HEAD~1")
        rows.append((number, text, status, description))
    return start, rows


def hidden_score(candidate, hidden_path):
    """Score a candidate file on the trainer's cases with the trusted prepare.py."""
    done = subprocess.run([sys.executable, "-B", "-c", HIDDEN_RUNNER, str(HERE),
                           str(candidate), str(hidden_path)], env=RUN_ENV,
                          capture_output=True, text=True, timeout=SECONDS)
    passed, total = done.stdout.split()
    return int(passed), int(total)


def report(ws, rows, start, hidden_path, out):
    """Print the table, the git log and the visible and hidden gain; write out."""
    table = "proposal\tscore\tstatus\tdescription\n" + "".join(
        f"{n}\t{score}\t{status}\t{text}\n" for n, score, status, text in rows)
    Path(out).write_text(table)
    print(f"\n{out}\n{table}")
    print("git log, oldest first (a reset proposal leaves no commit):")
    for subject in git(ws, "log", "--reverse", "--format=%s").splitlines():
        print(f"  {subject}")
    end, _ = evaluate(ws)
    counts = [sum(row[2] == status for row in rows)
              for status in ("keep", "discard", "rejected", "crash")]
    print(f"\nvisible score {start[0]}/{start[1]} at the start, {end[0]}/{end[1]} at "
          "the end: {} kept, {} reset, {} rejected, {} crashed".format(*counts))
    if not hidden_path:
        print("hidden set: not on this machine. The trainer holds it and shows "
              "the gap.")
        return
    first = hidden_score(HERE / MUTABLE, hidden_path)
    last = hidden_score(ws / MUTABLE, hidden_path)
    print(f"hidden set, 8 cases the proposer never saw: {first[0]}/{first[1]} at "
          f"the start, {last[0]}/{last[1]} at the end")
    print(f"gain on the visible cases {end[0] - start[0]:+d}, "
          f"gain on the hidden cases {last[0] - first[0]:+d}")


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--proposer", default="improve", choices=proposers.PROPOSERS)
    parser.add_argument("--budget", type=int, default=BUDGET)
    parser.add_argument("--rule-only", action="store_true")
    parser.add_argument("--hidden", help="path of the trainer's hidden_set.py")
    parser.add_argument("--out", default="results.tsv")
    args = parser.parse_args(argv)
    print(BANNER)
    print(f"ratchet: proposer {args.proposer}, budget {args.budget} proposals")
    print("rule: a proposal stays only if the visible score is strictly better")
    if args.rule_only:
        print("rule-only mode: the driver does not check the protected files")
    with tempfile.TemporaryDirectory(prefix="ratchet_") as root:
        ws = Path(root) / "ws"
        start_repo(ws)
        start, rows = run_loop(ws, proposers.PROPOSERS[args.proposer], args.budget,
                               args.rule_only)
        report(ws, rows, start, args.hidden, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
