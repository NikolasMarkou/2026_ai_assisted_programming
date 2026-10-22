"""Hook script: block reads of .env files. Reads one JSON event on stdin.

Exit 2 blocks the action and stderr goes back to the agent. Exit 0 allows it.
Fields used (names as the vendor docs list them, checked 2026-10-21):
  Claude Code and Codex, event PreToolUse: tool_input.file_path (Read, Edit, Write)
    and tool_input.command (Bash).
  Cursor, events beforeReadFile and beforeShellExecution: file_path and command.
A broken or missing event also blocks (fail closed). This is a guardrail and not a
security boundary: a command that builds the file name at run time gets through.
Each block is appended to guard.log in the event's cwd. Standard library only.
"""
import json
import os
import re
import sys

# .env, .env.local, prod.env as a whole file name; .env.example is allowed
BEFORE = r"(?:^|[\s\"'=<>/\\])"
AFTER = r"(?=$|[\s\"'|;&)])"
SECRET_NAME = re.compile(BEFORE + r"(\.env(?:\.[\w-]+)?|[\w-]+\.env)" + AFTER)


def secret_in(text):
    """Return the .env file name found in text, or None."""
    for name in SECRET_NAME.findall(text or ""):
        if not name.endswith(".example"):
            return name
    return None


def targets(event):
    """The strings of an event that can name a file: paths and shell commands."""
    inner = event.get("tool_input") or {}
    keys = ("file_path", "filePath", "command")
    values = [*(event.get(k) for k in keys), *(inner.get(k) for k in keys)]
    return [str(v) for v in values if v]


def log_block(folder, line):
    """Append a line to guard.log in folder. An unwritable folder is skipped."""
    try:
        with open(os.path.join(folder, "guard.log"), "a", encoding="utf-8") as log:
            log.write(line + "\n")
    except OSError:
        pass


def main():
    try:
        event = json.load(sys.stdin)
        if not isinstance(event, dict):
            raise ValueError("the event is not a JSON object")
    except ValueError as error:
        print(f"deny_env: cannot read the event ({error}); blocking", file=sys.stderr)
        return 2
    for text in targets(event):
        name = secret_in(" " + text)
        if name:
            who = event.get("tool_name") or event.get("hook_event_name")
            log_block(event.get("cwd") or os.getcwd(), f"BLOCKED {who} {name}")
            print(f"Blocked: reading {name} is denied by hooks/deny_env.py. "
                  "Secrets are not part of this task.", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
