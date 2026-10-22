# E12 answer key: plan, execute, verify with guardrails

Folder: `starter/exercises/e12`. Reference solution: `instructor/solutions/e12/` (3 files:
`report.py`, `cli.py`, `tests/test_report.py`). It adds 48 changed lines against the
starter; the limit in `check_done.py` is 80.

## What a correct run looks like

1. Plan checkpoint. The plan names 3 files (`report.py`, `cli.py`, `tests/test_report.py`)
   and says it will not touch `.env` or `migrations/`. Pairs that approve a plan without
   reading the file list have skipped the checkpoint. A plan that names `migrations/` is a
   reason to reject it.
2. Execute. `to_csv(items)` uses the `csv` module, so `Pen, blue` is written as
   `"Pen, blue"`. `export --low N` reuses `low_stock`, so it keeps the lowest-first order.
3. Verify. `python3 check_done.py` prints PASS on 4 checks (tests, diff within limit, no
   forbidden path changed, no forbidden path read) and `info  guard fired N times`.
4. Final diff checkpoint. The person reads `git diff`. Look for: a changed existing test,
   a new dependency, a change in `text_report` or `low_stock`, a stray file.

## The guardrail must fire

The task is done only when the guardrail fired at least once. Two easy ways:

- Ask the agent to "print the contents of .env". With the hook installed it is blocked
  (exit 2, message `Blocked: reading .env is denied by hooks/deny_env.py`), and
  `guard.log` gets a line. Without a hook the agent reads the fake file; the content is
  `FAKE_SECRET=not-a-real-secret`, so nothing is lost.
- Break a test on purpose. The `run_tests.py` hook reports the failing output to the agent
  right after the edit.

`check_done.py` prints the number of lines in `guard.log`. A pair with no hook shows a
"done means" rule in the instruction file instead; that is a prose rule and the agent may
ignore it. Ask them how they would know.

## Known holes (say them aloud)

| Hole | Why | Where it shows |
|---|---|---|
| `cat .e[n]v` passes `deny_env.py` | the script matches the text of the command, and the shell builds the name | `instructor/fallback_outputs/e12_guardrails_run.txt` |
| A Python script that opens `.env` passes it too | no file name appears in the command text | same, and demo d7 |
| The test hook cannot undo the edit | the tool already ran when PostToolUse fires | `hooks/README.md` |
| `check_done.py` reads `git diff` | an agent that commits its changes removes them from the diff; run it before any commit and check `git log` | the final diff checkpoint |
| Project hooks need the folder trusted | `claude -p` runs them with no dialog (ledger C-068, N-08) | the headless caveat |

## The retry cap (`pev.py`)

`python3 pev.py --agent "python3 never_green.py agent" --verify "python3 never_green.py verify"`
runs the agent once and then up to 2 fix attempts. The verify command needs a file
`approval.txt` that holds `signed`, which only a person can write, so it never turns
green. Expected: 3 agent runs, then the STOP report, exit 1. The recording is
`instructor/fallback_outputs/e12_pev_never_green.txt`. A third fix attempt would add a
fourth line to `attempts.log`: there is none. Stance: 2 fix attempts per failed step, then
stop and show the person what was tried and what failed.

## The semicolon demo

Demo d10 (`starter/demos/d10_shell_chain.py`) shows what one `;` does in a command the
agent wrote: after `git clone ... ; git sparse-checkout set a.py ; git checkout -q HEAD~1`
the file count in `git ls-files` is unchanged (3), the files on disk fall from 3 to 1, and
only the header of `git status` changes (HEAD detached, sparse checkout). With `&&` the
chain stops at the failed clone and the repository is unchanged. Use it to explain why a
check that looks at counts alone is not enough, and why the agent's shell commands need a
review before they run.

## Per tool

The config shapes in `hooks/README.md` were checked against vendor documentation on
2026-10-21 and were not run against the real tools. Ask a pair that tries one to report
what happened on the sheet. Ledger rows N-32 to N-49 in `content.md` hold the facts and the
items marked unverified.
