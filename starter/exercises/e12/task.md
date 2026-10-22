# E12 Task: add a CSV export to the stock list

The stock list prints a text report (`python3 cli.py report`). Add a CSV export.
The work touches 3 files: `report.py`, `cli.py` and `tests/test_report.py`.

## What to build

1. `report.py`: a function `to_csv(items)` that returns the CSV text of a list of items.
   The first line is `sku,name,qty,price`. Then one line per item, in the order given.
   `price` is in euros with 2 decimals, like `money()` prints it. Use the `csv` module of
   the standard library, so a name such as `Pen, blue` is quoted. Lines end with `\n`.
2. `cli.py`: a command `export` that prints the CSV of all items. `export --low N` prints
   only the items with a quantity below N, lowest quantity first, like the `low` command.
3. `tests/test_report.py`: tests for the header, the quoting of a name with a comma, the
   price format, `export` and `export --low`.

## Rules

- Do not read or change `.env`. Do not change anything under `migrations/`.
- Do not change the existing tests or the existing behaviour of `report` and `low`.
- The whole diff stays under 80 changed lines.

## Two human checkpoints

1. Plan approval. Before the agent changes a file it writes a plan: the files it will
   change and the tests it will add. You read it and answer yes or no. Write down what
   you changed in the plan, if anything.
2. Final diff. When the tests pass, run `git diff` and read the whole diff yourself. Then
   answer yes or no. Do not merge anything on the agent's word that it is done.

## Set up the guardrails first

- A deny rule for `.env` and a hook that runs the tests after each edit: copy the example
  for your tool from `hooks/` (see `hooks/README.md`).
- Tools without a hook: add the "done means" lines from `hooks/README.md` to your
  instruction file.
- Keep the retry cap: if the tests are still red after 2 fix attempts, stop the agent
  and read what it tried. `python3 pev.py` does this for you.

## Run it

```text
cp -r exercises/e12 e12_work && cd e12_work
git init -q -b main && git add -A && git commit -qm base
python3 -m unittest -q
```

Give your agent this file. After it finishes:

```text
python3 check_done.py
```

## Done when

- `check_done.py` prints PASS on all 4 checks.
- You recorded whether the guardrail fired: ask the agent to read `.env` and write down
  the block message, or that nothing blocked it, or break a test on purpose and see the
  hook report it. A guardrail that did not fire is a result to report.
- You approved or rejected at both checkpoints, and you can say which.
- If you can: run 2 attempts in separate branches or worktrees and keep the better diff.
