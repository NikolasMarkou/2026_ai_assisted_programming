# E3 Inside the loop

Task text for the agent, verbatim:

> The tests in tests/ fail. Find the bug, fix it and run the tests. Then say what you changed.

## Files

- `src/dates.py`: `parse_date` turns an ISO 8601 timestamp into a UTC `datetime`.
- `tests/test_dates.py`: 5 unittest cases. All 5 fail at the start.

Run the tests from this folder:

```text
python3 -m unittest -q
```

## What to do

1. Work on a copy so the starter stays clean: `cp -r exercises/e3 e3_work` (run from `starter/`).
2. Run `python3 agent/minimal_agent.py e3_work`. The offline scripted model answers, also if
   `ANTHROPIC_API_KEY` is set. Do not add `--live` today: it calls the paid API and gives a
   real model a shell with no sandbox.
3. Read the ACT and OBSERVE lines. Label each ACT line Action and each OBSERVE line
   Observation. In your own tool, also mark each Thought, the text before an action.
4. Run the same task in your own tool. Open its transcript or verbose view and its
   context-usage display, and compare the number of steps and the context size.

Done when every step in the trace is labelled and you have noted how much context the task used.
