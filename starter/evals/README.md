# Evals: a mini eval harness

`harness.py` runs an agent command on 10 small tasks, grades each run with hidden tests,
and reports the resolve rate, pass^k, the tamper rate and the wall time. Everything uses
Python 3.10 or newer, the standard library and git. Run commands from `starter/`.

| File | What it is |
|---|---|
| `harness.py` | The harness. One fresh workspace per trial, hidden tests added after the agent stops |
| `flaky_agent.py` | A scripted agent. Its behaviour on each task is drawn from a seeded distribution |
| `tasks/` | `tasks.json` and, per task, the base files: a module and its visible tests |
| `passk.py` | pass@k and pass^k from the closed form for one success rate |
| `labels_template.csv` | Columns for labelling failed trials by the part that failed |

The hidden tests are not in this folder. The trainer puts a folder named `hidden_evals` in
the shared folder for exercise E10 only. Copy it into `starter/` (next to `evals/`), pass
`--hidden hidden_evals`, and delete it after E10. `tasks.json` also holds the edits the
scripted agent makes.
Opening it shows what the scripted agent will do. It does not show the hidden tests.

## Run the scripted agent

```text
python3 evals/harness.py --configs baseline,run_tests_first --trials 3 --seeds 1-5 --out results \
  --hidden hidden_evals
```

A configuration is a name. The scripted agent reads it as its rule:

- `baseline`: the agent has no extra rule.
- `run_tests_first`: a rule that changes nothing. It draws from the same odds as `baseline`.
  Any gap between the two is noise.
- `real_effect`: a rule that lowers the chance that the agent gives up. A real effect of
  15 points exists. Compare it with `baseline` and see whether 10 tasks x 3 trials show it.

Seeds make a scripted run repeatable: the same seed gives the same table. The spread over
5 seeds is the size of the noise at 10 tasks x 3 trials.

## Read the table

| Column | Meaning |
|---|---|
| resolve | share of all trials where the hidden tests pass |
| pass^3 | share of tasks where all 3 trials passed (the number follows `--trials`) |
| tamper | share of trials that touched a protected path |
| escape | share of trials that left a file outside the workspace |
| timeouts | trials that hit `--timeout`; each counts as a failed trial |
| secs | wall time of the agent runs (leave it out with `--no-time`) |

Protected paths are `tests/`, `test_*.py`, `conftest.py`, `pyproject.toml` and `setup.cfg`.
The check reads `git status --porcelain` and `git diff --name-only <base>`, so a new
untracked file counts. A new test file you meant to add counts too.

## What each trial does

1. Copies the task's base files into a new temporary directory and makes a new git
   repository with one commit and no remote. `git log --all -p` shows only the base.
2. Runs the agent command in that directory with a timeout. A timeout kills the agent and
   its child processes, records a failed trial, and the harness goes on.
3. Lists the protected paths the agent touched, and any file left next to the workspace.
4. Copies the hidden tests in from outside the workspace (replacing any folder of that
   name the agent made) and runs them.

With `--out results` each trial writes a text file: the agent output, the paths it touched
and the test results. Use these files for the labelling step.

## Label the failures

Open the files of the failed trials of the first seed of your block of `baseline` (about
15 of the 30 trials).
For each, answer the 4 questions in `exercises/e9/diagnostic.md` and write one row in a
copy of `labels_template.csv`: `task, trial, outcome, failed part, note`. The failed part is one of knowledge and tools,
model, harness, sandbox. Count the rows per part.

## Run a real agent

This section is for the trainer and for use after E10. The folder `hidden_evals` is the
trainer's folder for E10 and is not part of this kit: do not point a real agent at it, and
delete it after E10. For a real agent, give `--hidden` hidden tests that the agent cannot
read, outside the container mount.

Run a real agent only inside a container or a throwaway directory with no real
credentials. It runs code from the tasks, and the harness gives it your environment.
Use one seed and few trials: a real agent is not seeded and each run costs time and money.

```text
python3 evals/harness.py --configs baseline --seeds 1 --trials 2 --tasks t01,t02,t03 \
  --hidden /path/to/hidden/tests \
  --agent-cmd 'claude --bare -p {prompt} --permission-mode acceptEdits --allowedTools "Bash,Read,Edit"'

python3 evals/harness.py --configs baseline --seeds 1 --trials 2 --tasks t01,t02,t03 \
  --hidden /path/to/hidden/tests \
  --agent-cmd 'codex exec --sandbox workspace-write {prompt}'
```

- Claude Code with `--bare` reads `ANTHROPIC_API_KEY` from the environment. Without a
  permission mode and `--allowedTools`, a headless run denies edits and shell commands.
- Codex `exec` starts in a read-only sandbox. Edits need `--sandbox workspace-write`.
- These flags were checked against the vendor documentation on 2026-10-21. The `codex`
  command was not installed on the machine that built this kit, so its line was never run
  here. Check `claude --help` and `codex exec --help` if a flag is rejected.

## Known limits

- A new file in the workspace root that is named like a standard library module is not a
  protected path, so the tamper check does not flag it.
- The harness cannot stop an agent from reading the folder given to `--hidden`. Mount only
  the workspace into the container.
- `escape` records files left next to the workspace and a changed canary file. It does not
  record a write to an absolute path elsewhere on the machine.
