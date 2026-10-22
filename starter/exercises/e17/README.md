# E17 The Ralph loop: a new context every pass, state in files

Everything here is scripted by the course authors. No model runs, nothing is measured
about real agents, and nothing leaves your machine. Every output starts with the line
`SCRIPTED DEMONSTRATION by the course authors, not a measurement`.

## The pattern

Geoffrey Huntley describes the loop in one line (https://ghuntley.com/ralph/, first
published 14 July 2025; he edited the page later):

```text
while :; do cat PROMPT.md | claude-code ; done
```

His words: "In its purest form, Ralph is a Bash loop." The command is spelled
`claude-code` in his post. The program is called `claude` today (our reading), so the
line is quoted as he wrote it and will not run as it stands.

What makes it work, in plain words:

| Idea | What it means here |
|---|---|
| State lives in files and git | `fix_plan.md` is the list of work, `progress.md` is the log, git holds the code. The agent forgets everything between passes and reads the files again. |
| A new context each pass | He says only about 170k of context window is usable and that more use gives worse results, so each pass starts empty. Every pass reads the same `PROMPT.md`. |
| One item per pass | He asks for "one thing per loop" and says you "may relax this restriction as the project progresses". He relaxes it himself in a later prompt, so it is a setting, not a law. |
| Backpressure from tests | "Anything can be wired in as back pressure to reject invalid code generation." Here the pass runs only the test class named on its item, and ticks the item only when that test passes. |
| A cap | His loop has no counter. Ours stops after 5 passes unless you set another number, and it refuses 0, a negative number and "no limit". |

He reports one case of a contract delivered at a small part of its price. It is one
self-reported case with no method. Do not plan from it. This kit gives no cost figure.

## What is in the folder

| File | Role |
|---|---|
| `PROMPT.md` | The prompt. Every pass reads it again. |
| `fix_plan.md` | 4 items. Items 1 to 3 are bugs in `items.py`. Item 4 cannot be fixed by code. |
| `items.py`, `test_items.py` | A tiny package with 3 bugs, and the tests the loop uses as backpressure. |
| `item_model.py` | The scripted model: it takes the first unchecked item, fixes it, runs that item's tests, ticks it and commits. It stops when a test fails. |
| `ralph.py` | The loop driver. One call of `agent()` per pass, with a new message list. |
| `ralph.sh` | The same loop in a POSIX shell. Windows needs WSL or Git Bash; `ralph.py` is the default. |
| `exit_hook_demo.py` | Our own illustration of the difference between this loop and a Stop hook. |

`ralph.py` works in a temporary copy of the four exercise files, with its own git
repository, and deletes it at the end. Your folder stays as it is. `--dir work` keeps
the copy in the folder `work`.

## Fresh context against a Stop hook

Anthropic's Ralph plugin repeats the prompt with a Stop hook. Its README says the loop
runs "inside your current session". That is a different design from the shell loop,
where each pass is a new process with a new context. `exit_hook_demo.py` runs both on
the same plan and prints how many context items each pass sends. It is our own
illustration of the difference, not a copy of any vendor's hook. Whether the plugin
compacts old messages is not something we tested.

The plugin has a cap: `--max-iterations <n>`, and its README says the default is
unlimited and to rely on that flag as the main safety mechanism. Claude Code also
stops a Stop hook that blocks eight times in a row with no tool call in between (Claude
Code documentation, hooks guide). Our driver does not rely on that; it counts passes.

## Steps

Run every command from the `starter/` folder.

1. Run the loop: `python3 exercises/e17/ralph.py`. Find the 3 passes that ticked an
   item and the 2 that did not. Read the numbers on the lines "context items sent".
   Why does the exit code say 1?
2. Run the cap case: `python3 exercises/e17/ralph.py --max-iterations 2`. Which items
   are still open when it stops, and where is that written down? Then try
   `--max-iterations 0` and read the answer.
3. Run `python3 exercises/e17/exit_hook_demo.py` and compare the two columns of message
   counts. What stayed the same in both runs, and what grew?

Done when you can say: why pass 4 and pass 5 changed nothing and what a person has to do
to fix item 4; what stopped the loop and why a loop without a cap would not stop;
where the state is kept between passes; and what the message count shows about the
difference between a new process per pass and one session.

## Notes

- Python 3.10 or newer and git are needed (`python3 check_env.py`). No network, no key.
- Try it for yourself: delete the line of item 4 from `fix_plan.md` in your copy and
  run step 1 again. The loop ends with exit 0 after 3 passes and says DONE.
- Play the person who unblocks item 4: run `python3 exercises/e17/ralph.py --dir work`,
  then `echo signed > work/approval.txt`, then run the same command again. Pass 6 ticks
  item 4 and the loop ends with DONE. Delete the folder `work` afterwards.
- `sh exercises/e17/ralph.sh` runs the same loop from a shell. If git changed the line
  endings of `ralph.sh` on Windows, run it with `bash` after `sed -i 's/\r$//' ralph.sh`.
- `--live` on `ralph.py` calls the real API. It needs `ANTHROPIC_API_KEY`, costs money
  and lets a real model run shell commands with no sandbox. Skip it in the exercise. A
  key in the environment never switches it on.
