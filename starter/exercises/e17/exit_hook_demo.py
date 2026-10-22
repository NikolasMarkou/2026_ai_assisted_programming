"""A new context every pass, against one growing session, scripted (exercise E17).

Usage: python3 exercises/e17/exit_hook_demo.py
Both runs get the same prompt, the same scripted model, the same fix_plan.md and 3
passes. The fresh run is what ralph.py does: every pass starts a new message list.
The session run is our own illustration of what a Stop hook does: when the agent
tries to finish, the exit is blocked and the same prompt is added to the same message
list. It is not a copy of any vendor's hook. The script prints the number of context
items sent in the last request of each pass. Nothing here measures a real model.
Interface for other code: hook_session(ws, model, passes) returns one pair (context
items sent in the last request, open items after the pass) per pass.
Standard library only.
"""
import contextlib
import io
import sys
import tempfile
from pathlib import Path

import ralph  # first: it puts agent/ on the import path
import item_model
import minimal_agent

PASSES = 3
TURNS = 30  # the same turn limit as minimal_agent.agent


def hook_session(ws, model, passes):
    """Run passes in one message list. Each end of turn is followed by the prompt."""
    task = (ws / "PROMPT.md").read_text(encoding="utf-8")
    messages, rows = [], []
    for _ in range(passes):
        messages.append({"role": "user", "content": task})
        for turn in range(TURNS):
            sent = len(messages)
            reply = model(messages)
            messages.append({"role": "assistant", "content": reply["content"]})
            if reply["stop_reason"] != "tool_use":
                break
            uses = [b for b in reply["content"] if b["type"] == "tool_use"]
            messages.append({"role": "user", "content": [
                minimal_agent.observe(b, turn, ws) for b in uses]})
        rows.append((sent, len(ralph.open_items(ws))))
    return rows


def quiet(function, *args):
    """Call function and drop what it prints."""
    with contextlib.redirect_stdout(io.StringIO()):
        return function(*args)


def main():
    print(ralph.BANNER)
    print("Our own illustration of two ways to repeat one prompt. It is not a copy "
          "of any vendor's hook.")
    print(f"Both runs: the same scripted model, the same fix_plan.md, {PASSES} passes.")
    print("  fresh context: an outer loop starts the agent again each pass "
          "(ralph.py, ralph.sh)")
    print("  one session:   a stop hook blocks the exit and adds the same prompt to "
          "the same list")
    with tempfile.TemporaryDirectory(prefix="hookdemo_") as root:
        fresh_ws, hook_ws = Path(root) / "fresh", Path(root) / "session"
        ralph.prepare(fresh_ws)
        ralph.prepare(hook_ws)
        fresh = quiet(ralph.run_loop, fresh_ws, item_model.call_model, PASSES)[1]
        hook = quiet(hook_session, hook_ws, item_model.call_model, PASSES)
    print("\nContext items sent in the last request of each pass:")
    print("pass  open items after  fresh context  one session")
    for (number, sent, _, after), (grown, open_after) in zip(fresh, hook):
        print(f"{number:<6}{after:<18}{sent:<15}{grown}")
        if after != open_after:
            sys.exit("the two runs did not fix the same items")
    print(f"\nIn both runs items 1 to {PASSES} were fixed, ticked in fix_plan.md and "
          "committed.")
    print("That state is in files and git. It does not depend on the message list.")
    print(f"The fresh run sent {fresh[0][1]} items in pass 1 and {fresh[-1][1]} in "
          f"pass {PASSES}. The session sent {hook[0][0]} and {hook[-1][0]}, because "
          "every earlier message stays in the list.")
    print("Our list never drops a message. A real session may compact or trim old "
          "messages; this script does not.")


if __name__ == "__main__":
    main()
