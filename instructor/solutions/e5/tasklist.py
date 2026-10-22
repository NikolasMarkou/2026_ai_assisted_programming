"""A task list stored in a JSON file. Standard library only.

Command line:
    python3 tasklist.py add TITLE [--due YYYY-MM-DD]
    python3 tasklist.py done ID
    python3 tasklist.py list [--overdue] [--today YYYY-MM-DD]
The file is tasks.json in the current directory unless TASKLIST_FILE is set.
"""
import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path


def load(path: str) -> list[dict]:
    """Return the list of tasks stored at path, or [] when the file does not exist."""
    file = Path(path)
    return json.loads(file.read_text()) if file.exists() else []


def save(path: str, tasks: list[dict]) -> None:
    Path(path).write_text(json.dumps(tasks, indent=2) + "\n")


def check_date(text: str) -> str:
    """Return text when it is a real YYYY-MM-DD date. Raises ValueError otherwise."""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        raise ValueError(f"'{text}' is not a date in the form YYYY-MM-DD")
    date.fromisoformat(text)
    return text


def add(tasks: list[dict], title: str, due: str | None = None) -> dict:
    """Append a task and return it. Raises ValueError for an empty title or bad date."""
    if not title.strip():
        raise ValueError("the title must not be empty")
    task = {"id": len(tasks) + 1, "title": title.strip(), "done": False}
    if due is not None:
        task["due"] = check_date(due)
    tasks.append(task)
    return task


def complete(tasks: list[dict], task_id: int) -> dict:
    """Mark the task with this id as done. Raises KeyError when there is none."""
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return task
    raise KeyError(task_id)


def overdue(tasks: list[dict], today: str) -> list[dict]:
    """Open tasks whose due date is before today (a YYYY-MM-DD string)."""
    return [t for t in tasks if not t["done"] and "due" in t and t["due"] < today]


def render(tasks: list[dict]) -> str:
    """One line per task, for example '[ ] 1 Write tests (due 2026-11-01)'."""
    marks = {True: "x", False: " "}
    lines = []
    for t in tasks:
        suffix = f" (due {t['due']})" if "due" in t else ""
        lines.append(f"[{marks[t['done']]}] {t['id']} {t['title']}{suffix}")
    return "\n".join(lines)


def parse(argv):
    parser = argparse.ArgumentParser(prog="tasklist.py")
    commands = parser.add_subparsers(dest="command", required=True)
    add_cmd = commands.add_parser("add")
    add_cmd.add_argument("title")
    add_cmd.add_argument("--due")
    commands.add_parser("done").add_argument("id", type=int)
    list_cmd = commands.add_parser("list")
    list_cmd.add_argument("--overdue", action="store_true")
    list_cmd.add_argument("--today", default=date.today().isoformat())
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    """Run one command. Returns the exit code: 0 on success, 1 on a bad value."""
    try:
        args = parse(argv)
    except SystemExit:
        return 1
    path = os.environ.get("TASKLIST_FILE", "tasks.json")
    tasks = load(path)
    try:
        if args.command == "add":
            add(tasks, args.title, args.due)
        elif args.command == "done":
            complete(tasks, args.id)
        else:
            shown = overdue(tasks, check_date(args.today)) if args.overdue else tasks
            print(render(shown))
            return 0
    except (ValueError, KeyError) as error:
        print(f"error: {error}")
        return 1
    save(path, tasks)
    print(render(tasks))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
