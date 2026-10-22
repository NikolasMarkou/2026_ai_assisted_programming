# Project: AI-assisted programming starter kit

## Stack
- Python 3.10 or newer, standard library only.
- Do not add dependencies without asking.

## Commands
- Test an exercise: run `python3 -m unittest -q` inside the exercise folder.
- Check the environment: `python3 check_env.py`
- Lint an instruction file: `python3 exercises/e5/lint_agents_md.py AGENTS.md`
- Run the offline agent on a copy of an exercise: `python3 agent/minimal_agent.py DIRECTORY`

## Rules
- Write or update the test before changing behavior.
- Run the tests after every change. Do not report done while a test fails.
- Do not edit a test to make it pass. If a test is wrong, say so and stop.
- Never print or log secrets. Secrets live in `.env`, which must not be read.
- Folders `agent/`, `demos/` and `exercises/` hold the kit. Change an exercise only
  inside its own folder.

## Done means
- All tests of the exercise pass, the diff has no unrelated changes, and the
  summary names every file you changed.
