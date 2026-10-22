"""Hook script: run the tests after a file edit. Reads one JSON event on stdin.

Exit 0 when the tests pass (nothing is printed). Exit 2 when they fail: stderr holds the
last lines of the test output, and the tool shows it to the agent. The event's cwd field
(Claude Code and Codex) names the folder; without it the current folder is used.
After an edit the tool has already run, so exit 2 cannot undo it; it only reports.

With --followup the script is a Cursor stop hook. On failure it prints a JSON object
with the key followup_message (Cursor sends it to the agent as the next message) and
exits 0. It prints nothing once loop_count reaches 2, so the agent gets 2 follow-ups.
Standard library only.
"""
import json
import subprocess
import sys

COMMAND = [sys.executable, "-m", "unittest", "-q"]
TAIL_LINES = 15
FOLLOWUP_CAP = 2


def main(followup):
    try:
        event = json.load(sys.stdin)
    except ValueError:
        event = {}
    event = event if isinstance(event, dict) else {}
    if followup and event.get("loop_count", 0) >= FOLLOWUP_CAP:
        return 0
    done = subprocess.run(COMMAND, cwd=event.get("cwd") or None, capture_output=True,
                          text=True, timeout=120)
    if done.returncode == 0:
        return 0
    tail = "\n".join((done.stderr + done.stdout).strip().splitlines()[-TAIL_LINES:])
    if followup:
        print(json.dumps({"followup_message": "Tests fail:\n" + tail}))
        return 0
    print("Tests fail after this edit:\n" + tail, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main("--followup" in sys.argv[1:]))
