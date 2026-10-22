# E19 Planner, workers and a judge: who may write which file

Everything here is scripted by the course authors. No model runs, nothing is measured
about real agents, and nothing leaves your machine. Every output starts with the line
`SCRIPTED DEMONSTRATION by the course authors, not a measurement`. There is no
`--live` option in this folder.

## The pattern

Cursor describes a way to run many coding agents at once in two blog posts by Wilson
Lin, its vendor research, not an independent test:

- January 2026, "Scaling long-running autonomous coding":
  https://cursor.com/blog/scaling-agents (page date 2026-01-14).
- February 2026, "Towards self-driving codebases":
  https://cursor.com/blog/self-driving-codebases (page date 2026-02-05).

The three roles come from the January post:

| Role | Words from the January post |
|---|---|
| planner | "Planners continuously explore the codebase and create tasks." |
| worker | "They don't coordinate with other workers or worry about the big picture." |
| judge | "At the end of each cycle, a judge agent determined whether to continue, then the next iteration would start fresh." |

The February post describes a later design and has no judge. It says: "We found agents
were reasonably good at following instructions to completion, so the judge was removed
to keep the system simple." So the judge is a role you may add, not a part every
version of the design has. In the February design a worker works on its own copy of
the repo and, when it is done, will "write up a single handoff" for the planner that
asked for the task. This exercise has one handoff line per worker.

Locks against ownership, in our words (a paraphrase, not a sentence from either post):
the January post reports that a first design, where agents of equal status coordinated
through one shared file, slowed 20 agents down to the effective throughput of "two or
three". The design that followed gave each planner a slice of the work to own, and
workers did not coordinate with each other. The posts say nothing about a laptop, and
the kit produces no figure from them.

## What is in the folder

| File | Role |
|---|---|
| `shop/` | A small order package. `interface.py` is shared and only the planner may change it. `parse.py`, `total.py` and `render.py` are three stubs, one per slice. `test_shop.py` has one test class per slice. |
| `planner.py` | The scripted planner: splits the task into slices a, b and c and writes `ownership.json` (the files each worker owns). Also finds a file that two slices claim. |
| `worker.py` | The scripted worker: finishes its own stub and writes one handoff line. It asks for edits; it does not write files. |
| `judge.py` | The scripted judge: runs the test class of each slice and says CONTINUE or STOP with a reason. |
| `team.py` | The driver: planner, three workers, judge, one round. It applies a worker's edit only to a file its slice owns and refuses every other write. |
| `overlap.json` | A plan in which two slices both claim `shop/total.py`. |
| `lock_toy.py` | A toy simulation: 20 workers on one shared lock against 20 workers who each own a file. |

`team.py` works in a temporary copy of `shop/` and deletes it at the end. `--dir work`
keeps the copy in a new folder `work`, with `ownership.json` and `handoff.md`.

## Steps

Run every command from the `starter/` folder.

1. Run the team: `python3 exercises/e19/team.py`. Read `ownership.json`, the three
   handoff lines and the judge table. Which files changed, and which file could no
   worker change?
2. Run the overlap case: `python3 exercises/e19/team.py --plan exercises/e19/overlap.json`.
   Find the line that names the conflict. Did a worker start? What does the judge say?
3. Run the toy: `python3 exercises/e19/lock_toy.py`. Read the two numbers in the column
   "tasks finished" and the share of time spent waiting. Which rule makes the first
   number smaller?

Done when you can say: why each worker could finish without knowing about the other
two; what the driver would have done if worker b had written `shop/interface.py`;
what the judge looked at before it said STOP (counts from the tests, not the code);
why the overlap plan never reached a worker; and what the two toy numbers depend on.

## Notes

- Python 3.10 or newer is needed (`python3 check_env.py`). No network, no key, no git.
- `team.py` exits 0 when the judge says STOP with every test passing, and 1 for any
  other result, so the overlap case exits 1 on purpose.
- Try for yourself: `--skip c` (worker c never reports: the judge says CONTINUE and
  names slice c), `--rogue b` (worker b also asks to change `shop/interface.py`: the
  driver refuses that write), and `--workers 1` or `--workers 5` on the toy.
- The planner is a fixed script. A real planner would read the repository and decide
  the split, and it could get the split wrong. The judge reads test counts only; it
  gives no opinion on the code.
- The toy is our own set of rules. Its numbers tell you what these rules produce, not
  what any real lock or any real agents do. Change a number at the top of
  `lock_toy.py` and run it again to see what moves.
- Both posts are a vendor describing its own system. Whether this split works for a
  small team on one repository is not something they, or this exercise, test.
