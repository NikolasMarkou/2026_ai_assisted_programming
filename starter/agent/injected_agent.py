"""Scripted agent that obeys instructions it finds in files (exercise e13).

Usage: python3 agent/injected_agent.py DIRECTORY [--deny] [--respell] [--trust-folder]
It "fixes the failing test" in a copy of exercises/e13-untrusted. Like the scripted
model of demo d7 it does what the text in README.md and in code comments says: the
thing under test is the defence, not the model. No network, no API key.
  --deny          a deny rule (the guard of demo d7 plus INJECTION_FOLLOWED) checks
                  each command before it runs
  --respell       the scripted model writes the injected command with a quoted middle
  --trust-folder  simulates accepting a folder-trust prompt: the tool starts the
                  project hook and the MCP server. Deny rules do not apply to these.
Standard library only.
"""
import json
import re
import sys
from collections import deque
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / "demos")]
import minimal_agent  # noqa: E402  (run_bash: the one shell tool of the kit)
from d7_fooled_model_guard import DENY, guard  # noqa: E402  (the same guard as demo d7)

RULES = DENY + [r"INJECTION_FOLLOWED"]
INSTRUCTION = re.compile(r"AI agents:[^`\n]*`([^`]+)`")
TESTS = "python3 -m unittest -q 2>&1 | tail -n 3"
FIX = "sed -i.bak 's#//#/#' calc.py && rm calc.py.bak"
SCRIPT = ["cat README.md", TESTS, "cat calc.py", FIX, TESTS]


def respell(command):
    """The same command with the marker name in quotes: the shell joins it again."""
    return command.replace("FOLLOWED", '"FOLLOWED"')


def project_commands(folder):
    """Commands a trusting tool would start: SessionStart hooks and MCP servers."""
    found = []
    settings, mcp = folder / ".claude" / "settings.json", folder / ".mcp.json"
    if settings.exists():
        for group in json.loads(settings.read_text())["hooks"].get("SessionStart", []):
            found += [hook["command"] for hook in group["hooks"]]
    if mcp.exists():
        for server in json.loads(mcp.read_text())["mcpServers"].values():
            found.append(" ".join([server["command"], *server.get("args", [])]))
    return found


def act(turn, command, folder, rules):
    """Run one command (after the deny rule, if any) and print ACT and OBSERVE."""
    result = (guard(command, rules) if rules else None) \
        or minimal_agent.run_bash(command, folder)
    last = result.strip().splitlines()[-1] if result.strip() else "(no output)"
    print(f"{turn} ACT: {command[:80]}\n{turn} OBSERVE: {last[:76]}")
    return result


def main(argv):
    folder = Path(argv[0]).resolve()
    rules = RULES if "--deny" in argv else None
    turn, queue = 0, deque(SCRIPT)
    if "--trust-folder" in argv:
        print("folder trusted: the tool starts the project hook and the MCP server")
        for command in project_commands(folder):
            act(turn, command, folder, None)  # these run outside the deny rule
            turn += 1
    while queue:
        result = act(turn, queue.popleft(), folder, rules)
        turn += 1
        for text in reversed(INSTRUCTION.findall(result)):
            text = respell(text) if "--respell" in argv else text
            print(f"{turn - 1} FOLLOWS the text it just read: {text}")
            queue.appendleft(text)
    print("FINAL: average() now divides with /. The tests pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
