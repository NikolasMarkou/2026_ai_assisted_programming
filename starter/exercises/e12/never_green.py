"""A task that can never turn green, to show the retry cap.

    python3 pev.py --agent "python3 never_green.py agent" \
        --verify "python3 never_green.py verify"

verify needs a file approval.txt that holds the word signed, and only a person may
write it. The agent tries something different each time and cannot make it pass. Each
agent run adds one line to attempts.log, so a third fix attempt would be visible.
"""
import os
import sys
from pathlib import Path

TRIES = ["edited my notes file", "ran the tests again", "changed the check in my plan",
         "asked for another attempt"]


def agent():
    attempt = int(os.environ.get("PEV_ATTEMPT", "0"))
    with open("attempts.log", "a", encoding="utf-8") as log:
        log.write(f"agent run, attempt {attempt}\n")
    print(f"attempt {attempt}: {TRIES[attempt % len(TRIES)]}")
    return 0


def verify():
    path = Path("approval.txt")
    if path.exists() and path.read_text().strip() == "signed":
        print("approval found")
        return 0
    print("FAIL: approval.txt is not signed. Only a person signs it.")
    return 1


if __name__ == "__main__":
    sys.exit({"agent": agent, "verify": verify}[sys.argv[1]]())
