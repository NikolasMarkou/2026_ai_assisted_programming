# E16 The ratchet: keep a change only if the score is strictly better

Everything here is scripted by the course authors. No model runs, nothing is measured
about real agents, and nothing leaves your machine. Every output starts with the line
`SCRIPTED DEMONSTRATION by the course authors, not a measurement`.

## The pattern

An agent works on code in a loop. Each round it changes the code, a fixed program
scores the result, and the change stays only if the score is strictly better than the
best so far. Otherwise the code goes back to the previous commit. The history then holds
only changes that raised the score.

Karpathy's autoresearch repository (https://github.com/karpathy/autoresearch) uses this
loop with three files:

| File here | Role | Who edits it |
|---|---|---|
| `candidate.py` | The one file the agent changes. In his repository it is `train.py`. | The agent |
| `prepare.py` | The evaluator. It prints the score. His README marks the file "do not modify". | Nobody during the run |
| `program.md` | The rules and the loop in plain text. | The human |

Here the task is small: `parse_price` turns `"$1,200.75"` into `120075` cents. The score
is how many of 8 visible cases it gets right. The budget is 6 proposals. A proposer is a
fixed script that returns new file texts; `ratchet.py` is the loop around it. It makes a
temporary git repository, commits each proposal, runs `python3 prepare.py`, keeps the
commit or resets, and writes `results.tsv`. The temporary repository is deleted at the end.

## Why "frozen" is only a rule

`program.md` tells the agent not to edit `prepare.py`. A rule in a text file stops
nothing. Here `prepare.py` sits next to `candidate.py`, and the agent reads the number
that the run prints. In his repository, by our reading of the code (an inference, not a
statement of his), `train.py` imports the scoring function and prints the line that the
agent reads. Karpathy does not describe a gaming risk himself. Two third-party reports
do. We read them and do not reproduce them here:

- Issue 64 on that repository, opened by a user who is not the author, says the run log
  can carry crafted text to the agent (https://github.com/karpathy/autoresearch/issues/64).
- A paper on a similar loop for a different task reports that one agent hard-coded
  validation answers, and that the effect vanished once a held-out set was added
  (https://arxiv.org/abs/2607.18064).

Our driver enforces the rule with a check: it records the sha256 of `prepare.py` and
`program.md` before the first proposal, and it rejects any proposal that changes them or
changes any file except `candidate.py`. That check is a part of our driver. It is not in
the file, and `--rule-only` switches it off so you can see what the rule alone does.

## The limit of the visible score

The score is computed on 8 visible cases. A candidate that copies those 8 answers gets
8 of 8 and still cannot parse a price it has not seen. The trainer holds a second set of
8 hidden cases of the same task. The improving candidate rises on both sets; the copying
candidate rises on the visible set only. A visible score that went up is evidence of a
better candidate only while the cases stay unseen by the proposer.

## Steps

Run every command from the `starter/` folder. `ratchet.py` writes `results.tsv` there;
delete it when you finish.

1. Run the ratchet with the improving proposer: `python3 exercises/e16/ratchet.py`. Find the 2 proposals that
   were reset. One of them did not lower the score. Why was it reset? Count the
   commits in the git log at the end.
2. Run the two gaming proposers, one after the other:
   `python3 exercises/e16/ratchet.py --proposer edit_evaluator` and
   `python3 exercises/e16/ratchet.py --proposer hardcode`. Which check stopped the first
   one? What is the visible score of the second? The trainer runs it with the hidden set
   and shows the second score.
3. Run `python3 exercises/e16/run_log_demo.py`. A package that `candidate.py` imports
   printed one line into the run log. Say which line was an instruction, which proposer
   acted on it, and what the summary kept.

Done when you can say: why an equal score is reset; what stopped the evaluator edit and
what would have let it through; why 8 of 8 on the visible cases says nothing about the
hidden cases; and why the summary removes the injected line while `program.md` did not.

## Notes

- Python 3.10 or newer and git are needed (`python3 check_env.py`). No network, no key.
- `--rule-only` is optional: run `python3 exercises/e16/ratchet.py --proposer
  edit_evaluator --rule-only` and compare.
- Your own agent could play the proposer, but it would need a sandbox first. This
  exercise gives it none.
