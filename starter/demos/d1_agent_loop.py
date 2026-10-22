"""Demo 1: a coding agent loop with a scripted model and a real bash tool.

Standard library only. No key, no network. The scripted model replays the
messages a real model might send, one per turn, and does not read what it is sent.
"""
import json
import os
import subprocess
import tempfile
from pathlib import Path

# sed keeps size and mtime second, so a stale .pyc would hide the fix.
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

workdir = tempfile.TemporaryDirectory()
repo = Path(workdir.name)
# The bug: the slice takes 3 characters of the year, it should take 4.
(repo / "dates.py").write_text("def year(s):\n    return int(s[:3])\n")
(repo / "test_dates.py").write_text(
    "from dates import year\nassert year('2026-10-22') == 2026\nprint('ok')\n")

SCRIPT = iter([
    {"command": "python3 test_dates.py"},
    {"command": "cat dates.py"},
    {"command": "sed -i.bak 's/s\\[:3\\]/s[:4]/' dates.py && rm dates.py.bak"},
    {"command": "python3 test_dates.py"},
    {"final": "Fixed the slice in year(); the test prints ok."},
])


def fake_model(messages):
    return next(SCRIPT)


def run_bash(command):
    r = subprocess.run(command, shell=True, cwd=repo, capture_output=True,
                       text=True, timeout=20)
    return (r.stdout + r.stderr)[-2000:] or "(no output)"


messages = [{"role": "user", "content": "test_dates.py fails. Fix it."}]
seen = []
for turn in range(10):  # the turn limit
    reply = fake_model(messages)
    messages.append({"role": "assistant", "content": json.dumps(reply)})
    if "final" in reply:
        print(f"[turn {turn}] FINAL: {reply['final']}")
        break
    out = run_bash(reply["command"])
    seen.append(out.strip().splitlines()[-1].strip())
    print(f"[turn {turn}] ACT: {reply['command']}")
    print(f"          OBSERVE: {seen[-1][:60]}")
    messages.append({"role": "user", "content": out})
print("context items after the run:", len(messages))
check = run_bash("python3 test_dates.py").strip()
print("check run by the harness itself:", check)

# Hidden check (not shown)
assert len(messages) == 10
assert seen == ["AssertionError", "return int(s[:3])", "(no output)", "ok"]
assert check == "ok"
assert (repo / "dates.py").read_text() == "def year(s):\n    return int(s[:4])\n"
workdir.cleanup()
