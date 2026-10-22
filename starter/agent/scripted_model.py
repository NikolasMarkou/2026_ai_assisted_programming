"""Offline stand-in for the Messages API. It returns the same response shape.

call_model(messages) takes the message list the agent would send and returns a
dict with "content" (text and tool_use blocks) and "stop_reason". It keeps no
state: each answer is a rule applied to the last tool_result in messages.
The rules fix exercise e3 (a date parser that drops the UTC offset). On any other
task, or on output no rule matches, it stops and says so.
Standard library only.
"""
import re

RUN_TESTS = "python3 -m unittest -q 2>&1 | tail -n 15"
RERUN_TESTS = "python3 -m unittest -q 2>&1 | tail -n 3"
FIX = "sed -i.bak '$s/replace(tzinfo=/astimezone(/' {path} && rm {path}.bak"
BUGGY_LINE = "return moment.replace(tzinfo=timezone.utc)"


def last_result(messages: list) -> str | None:
    """Text of the last tool_result, or None before the first tool call."""
    content = messages[-1]["content"]
    if isinstance(content, str):
        return None
    return "\n".join(block["content"] for block in content)


def last_command(messages: list) -> str:
    """The command of the last assistant tool_use, or an empty string."""
    for message in reversed(messages):
        if message["role"] == "assistant":
            uses = [b for b in message["content"] if b["type"] == "tool_use"]
            return uses[-1]["input"]["command"] if uses else ""
    return ""


def decide(messages: list) -> tuple[str, str | None]:
    """Return (text, command). command is None when the task is finished."""
    result = last_result(messages)
    if result is None:
        return "I will run the tests to see what fails.", RUN_TESTS
    called = re.search(r"assert\w*\((\w+)\(", result) if "Traceback" in result else None
    if called:
        return (f"The failing assertion calls {called[1]}. I will find its definition.",
                f'grep -rn "def {called[1]}" --include=*.py .')
    defined = re.match(r"(\S+?):\d+:def (\w+)", result)
    if defined:
        return (f"{defined[2]} is defined in {defined[1]}. I will read it.",
                f"cat {defined[1].removeprefix('./')}")
    if BUGGY_LINE in result:
        return ("The last line labels the datetime as UTC without converting it. "
                "astimezone converts the value.",
                FIX.format(path=last_command(messages).split()[-1]))
    if result == "(no output)" and last_command(messages).startswith("sed"):
        return "The edit is in. I will run the tests again.", RERUN_TESTS
    if result.rstrip().endswith("OK"):
        return "parse_date now converts the offset to UTC. All tests pass.", None
    if "FAILED" in result:
        return "The tests still fail. I am stopping so you can look.", None
    return "No rule matches this output, so I am stopping.", None


def call_model(messages: list) -> dict:
    """Return an API-shaped response for the messages sent so far."""
    text, command = decide(messages)
    content = [{"type": "text", "text": text}]
    if command is None:
        return {"content": content, "stop_reason": "end_turn"}
    call_id = f"toolu_scripted_{len(messages):02d}"
    content.append({"type": "tool_use", "id": call_id, "name": "bash",
                    "input": {"command": command}})
    return {"content": content, "stop_reason": "tool_use"}
