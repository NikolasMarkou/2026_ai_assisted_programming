"""Scripted model for exercise E17: it works the first unchecked item of fix_plan.md.

call_model(messages) takes the message list the agent would send and returns an
API-shaped response: "content" (text and tool_use blocks) and "stop_reason". It keeps
no state. Each answer is a rule applied to the last tool_result and the last command:
  start of a pass (the last message is the prompt text): read the first unchecked
      item of fix_plan.md
  plan read: take that item. If FIXES has a fix for it, apply the fix.
      If not, run its test.
  fix applied: run the test class of that item only (the backpressure)
  test ends in OK: tick the item, then commit items.py and fix_plan.md
  test fails: stop without ticking the item
  commit done: stop. One item per pass.
Standard library only.
"""
import re

READ_PLAN = "grep '^- \\[ \\]' fix_plan.md | head -n 1"  # the first unchecked item
GIT = ("git -c user.name=ralph -c user.email=ralph@example.invalid "
       "-c commit.gpgsign=false")
UNIT = "python3 -m unittest -q test_items.{} 2>&1 | tail -n 3"
EDIT = "sed -i.bak '{}' items.py && rm items.py.bak"
NAMES = {1: "clean_name keeps one space between words",
         2: "to_cents rounds to the nearest cent",
         3: "largest returns the biggest values first",
         4: "release needs a signed approval.txt"}
TESTS = {1: "TestCleanName", 2: "TestToCents", 3: "TestLargest", 4: "TestRelease"}
FIXES = {  # item 4 has no entry: no edit of the code can fix it
    1: EDIT.format('s/return text.replace(" ", "")/return " ".join(text.split())/'),
    2: EDIT.format(r's/return int(float(text) \* 100)/'
                   r'return round(float(text) * 100)/'),
    3: EDIT.format(r's/return sorted(values)\[:n\]/'
                   r'return sorted(values, reverse=True)[:n]/'),
}


def test_command(number):
    return UNIT.format(TESTS[number])


def done_command(number):
    """Tick item number in fix_plan.md, then commit the two files that changed."""
    tick = (rf"sed -i.bak 's/^- \[ \] {number}\./- [x] {number}./' fix_plan.md "
            "&& rm fix_plan.md.bak")
    return (f"{tick} && {GIT} add items.py fix_plan.md "
            f"&& {GIT} commit -q -m 'item {number}: {NAMES[number]}'")


BY_FIX = {command: number for number, command in FIXES.items()}
BY_TEST = {test_command(number): number for number in TESTS}
BY_DONE = {done_command(number): number for number in TESTS}


def last_result(messages: list) -> str | None:
    """Text of the last tool_result, or None while the last message is the prompt."""
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
    """Return (text, command). command is None when the pass is finished."""
    result, command = last_result(messages), last_command(messages)
    if result is None:
        return "I will read the plan.", READ_PLAN
    if command == READ_PLAN:
        found = re.search(r"^- \[ \] (\d+)\. (.*)$", result, re.M)
        if not found:
            return "No unchecked item is left. There is nothing to do.", None
        number = int(found[1])
        if number in FIXES:
            return (f"Item {number} is the first unchecked one: "
                    f"{found[2].split(' (test')[0]}. I will fix it.", FIXES[number])
        return (f"Item {number} is the first unchecked one. I will run its test "
                "to see what fails.", test_command(number))
    if command in BY_FIX:
        number = BY_FIX[command]
        return (f"The edit for item {number} is in. I run its test class only.",
                test_command(number))
    if command in BY_TEST:
        number = BY_TEST[command]
        if result.rstrip().endswith("OK"):
            return (f"The test for item {number} passes. I tick the item and commit.",
                    done_command(number))
        if number in FIXES:
            return (f"The test for item {number} still fails. I stop without "
                    "ticking it.", None)
        return (f"Item {number} fails because approval.txt is not signed, and only a "
                "person may write it. No edit of mine can pass this test. I leave "
                "the item unchecked.", None)
    if command in BY_DONE:
        return (f"Item {BY_DONE[command]} passes its test, is ticked and is committed. "
                "I stop here so the next pass starts with a new context.", None)
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
