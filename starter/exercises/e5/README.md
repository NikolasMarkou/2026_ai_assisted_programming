# E5 Persisted context

Files in this folder:

- `tasklist.py` and `tests/test_tasklist.py`: a small task list to extend. All tests pass at the start.
- `feature_request.md`: the feature to add, in plan mode.
- `lint_agents_md.py`: checks an AGENTS.md against the folder it sits in.

Steps:

1. Write `AGENTS.md` in this folder: stack, commands, rules, done means.
2. Run `python3 lint_agents_md.py AGENTS.md`. Fix every GONE, MISSING and TOO LONG line.
3. Re-run one prompt from E4 with and without the file and compare the results.
4. Run the feature request in plan mode: review and edit the plan, then execute.

Run the tests from this folder with `python3 -m unittest -q`.
Done when your AGENTS.md passes the lint and you can name one behaviour it changed.
