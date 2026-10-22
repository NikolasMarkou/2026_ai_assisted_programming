"""Minimal coding agent: one tool (bash), one loop, standard library only.

Usage: python3 agent/minimal_agent.py DIRECTORY [--live]   (--live may also come first)
The offline model in scripted_model.py answers, also when ANTHROPIC_API_KEY is set. Only
--live calls the Messages API: it needs the key, costs money, and lets a real model run
shell commands in DIRECTORY with no sandbox. Either way the agent runs shell commands
in DIRECTORY, so give it a copy of the exercise folder. The shell tool does not inherit
variables whose names contain KEY, TOKEN, SECRET or PASSWORD. That does not hide the key
from a live model: the agent process still holds it, and a shell command can read the
environment of its parent process (on Linux, /proc/$PPID/environ). Run --live in a
container.
"""
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

import scripted_model

MODEL = "claude-sonnet-5-5"
TASK = ("The tests in tests/ fail. Find the bug, fix it and run the tests. "
        "Then say what you changed.")
SYSTEM = ("You are a coding agent in the current directory. Inspect before editing. "
          "After every change run the tests. Finish only when they pass.")
PYTHON_DIR = str(Path(sys.executable).parent)  # the shell finds the same python3
SECRET_WORDS = ("KEY", "TOKEN", "SECRET", "PASSWORD")  # variables the shell never gets
ENV = {**{k: v for k, v in os.environ.items()
          if not any(word in k.upper() for word in SECRET_WORDS)},
       "PYTHONDONTWRITEBYTECODE": "1",
       "PATH": PYTHON_DIR + os.pathsep + os.environ.get("PATH", "")}
TOOLS = [{
    "name": "bash",
    "description": "Run a shell command in the working directory. Returns stdout and "
                   "stderr together. Use it to read, search, edit and test.",
    "input_schema": {
        "type": "object",
        "properties": {"command": {"type": "string", "description": "Shell command"}},
        "required": ["command"],
    },
}]


def run_bash(command: str, cwd: Path) -> str:
    # A real harness checks permissions before this call and runs it in a sandbox.
    try:
        done = subprocess.run(command, shell=True, cwd=cwd, env=ENV, timeout=120,
                              capture_output=True, text=True)
    except subprocess.TimeoutExpired:
        return "error: the command ran longer than 120 s and was stopped"
    return (done.stdout + done.stderr)[-10_000:] or "(no output)"


def call_model(messages: list, max_tokens: int = 8192) -> dict:
    """POST the messages to the Messages API; return the response as a dict.

    The dict has "content" (a list of blocks) and "stop_reason". Exits with the
    HTTP status and the start of the error body when the API answers with an error,
    and with one line when the API cannot be reached.
    """
    base = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
    body = {"model": MODEL, "max_tokens": max_tokens, "system": SYSTEM,
            "tools": TOOLS, "messages": messages}  # no temperature: it gets HTTP 400
    headers = {"content-type": "application/json",
               "x-api-key": os.environ["ANTHROPIC_API_KEY"],
               "anthropic-version": "2023-06-01"}
    request = urllib.request.Request(base.rstrip("/") + "/v1/messages",
                                     json.dumps(body).encode(), headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=300) as reply:
            return json.load(reply)
    except urllib.error.HTTPError as error:
        sys.exit(f"API error {error.code}: {error.read().decode()[:300]}")
    except (urllib.error.URLError, TimeoutError) as error:  # no network, proxy, timeout
        sys.exit(f"cannot reach the API: {getattr(error, 'reason', error)}")


def observe(block: dict, turn: int, cwd: Path) -> dict:
    """Run one tool_use block, print ACT and OBSERVE, return its tool_result."""
    command = block["input"]["command"]
    output = run_bash(command, cwd)
    last = (output.strip().splitlines() or [output])[-1].replace(str(cwd), ".")
    print(f"{turn} ACT: {command[:80]}\n{turn} OBSERVE: {last.strip()[:76]}")
    return {"type": "tool_result", "tool_use_id": block["id"], "content": output}


def finish(resp: dict) -> None:
    """Print the final text; print the stop reason unless it is end_turn."""
    for block in resp["content"]:
        if block["type"] == "text":
            print("FINAL:", block["text"])
    if resp["stop_reason"] != "end_turn":
        print(f"stopped: {resp['stop_reason']}")


def agent(task: str, cwd: Path, call_model=call_model, max_turns: int = 30) -> int:
    """Run the loop; return how many context items the last request carried."""
    messages = [{"role": "user", "content": task}]
    for turn in range(max_turns):
        sent = len(messages)  # items the model receives this turn
        resp = call_model(messages)
        messages.append({"role": "assistant", "content": resp["content"]})
        if resp["stop_reason"] != "tool_use":  # end_turn, max_tokens, refusal, ...
            finish(resp)
            return sent
        uses = [b for b in resp["content"] if b["type"] == "tool_use"]
        results = [observe(b, turn, cwd) for b in uses]  # tool_result blocks go first
        messages.append({"role": "user", "content": results})
    print("stopped: turn limit")
    return sent


def main(directory: str, live: bool = False) -> None:
    """Run the task in directory. live=True calls the API; the default is offline."""
    if live and not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("--live needs ANTHROPIC_API_KEY in the environment")
    print("model:", MODEL if live else "scripted (offline)")
    if live:
        print("warning: live run. The task goes to the API with your key, and the "
              "model runs shell commands in this folder with no sandbox.")
    model = call_model if live else scripted_model.call_model
    sent = agent(TASK, Path(directory).resolve(), model)
    print("context items sent in the last request:", sent)


if __name__ == "__main__":
    flags = {arg for arg in sys.argv[1:] if arg.startswith("--")}
    folders = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    if len(folders) != 1 or flags - {"--live", "--scripted"}:
        sys.exit(__doc__)
    if flags == {"--live", "--scripted"}:
        sys.exit("choose one of --live and --scripted")
    main(folders[0], live="--live" in flags)
