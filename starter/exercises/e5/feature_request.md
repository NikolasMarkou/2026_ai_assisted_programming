# Feature request: due dates

Users want to give a task a due date and to see which open tasks are late.

## Behaviour

1. `python3 tasklist.py add "Write tests" --due 2026-11-01` stores the due date with the task.
   A task added without `--due` has no due date. A date that is not `YYYY-MM-DD` is rejected
   with exit code 1 and a message, and nothing is stored.
2. `list` shows the due date after the title: `[ ] 1 Write tests (due 2026-11-01)`.
   Tasks without a due date show no suffix.
3. `python3 tasklist.py list --overdue --today 2026-11-02` shows only open tasks whose
   due date is before the `--today` date. `--today` defaults to the current date.
   A done task is never overdue. A task due on the `--today` date is not overdue.

## Constraints

- Standard library only. Do not change the shape of tasks already stored in tasks.json:
  a file written by the current version must still load.
- Existing tests keep passing. New behaviour comes with new tests in `tests/`.

## How to work

1. Write `AGENTS.md` for this folder first (stack, commands, rules, done means).
2. Ask the agent for a plan, read it, edit it, then let it execute.
3. Check the result with `python3 -m unittest -q` and `python3 lint_agents_md.py AGENTS.md`.
