"""A task list stored in a JSON file. Standard library only.

Command line: python3 tasklist.py add TITLE | done ID | list
The file is tasks.json in the current directory unless TASKLIST_FILE is set.
"""
import json
import os
import sys
from pathlib import Path


def load(path: str) -> list[dict]:
    """Return the list of tasks stored at path, or [] when the file does not exist."""
    file = Path(path)
    return json.loads(file.read_text()) if file.exists() else []


def save(path: str, tasks: list[dict]) -> None:
    Path(path).write_text(json.dumps(tasks, indent=2) + "\n")


def add(tasks: list[dict], title: str) -> dict:
    """Append a task and return it. Raises ValueError when the title is empty."""
    if not title.strip():
        raise ValueError("the title must not be empty")
    task = {"id": len(tasks) + 1, "title": title.strip(), "done": False}
    tasks.append(task)
    return task


def complete(tasks: list[dict], task_id: int) -> dict:
    """Mark the task with this id as done. Raises KeyError when there is none."""
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return task
    raise KeyError(task_id)


def render(tasks: list[dict]) -> str:
    """One line per task, for example '[x] 2 Write tests'."""
    marks = {True: "x", False: " "}
    return "\n".join(f"[{marks[t['done']]}] {t['id']} {t['title']}" for t in tasks)


def main(argv: list[str]) -> int:
    """Run one command. Returns the exit code: 0 on success, 1 on a bad command."""
    path = os.environ.get("TASKLIST_FILE", "tasks.json")
    tasks = load(path)
    if argv[:1] == ["add"] and len(argv) == 2:
        add(tasks, argv[1])
    elif argv[:1] == ["done"] and len(argv) == 2:
        complete(tasks, int(argv[1]))
    elif argv != ["list"]:
        print("usage: tasklist.py add TITLE | done ID | list")
        return 1
    save(path, tasks)
    print(render(tasks))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
