# E18 The loop spec: five parts you write down before the loop runs

Everything here is scripted by the course authors. No model runs, nothing is measured
about real agents, and nothing leaves your machine. The run in step 3 starts with the
line `SCRIPTED DEMONSTRATION by the course authors, not a measurement`.

## The pattern

In E17 you ran a loop that someone had already set up: a prompt, a plan file, a cap.
A loop spec is that setup written down as one reusable file that you hand to an agent
harness. It answers five questions:

| Part | The question it answers |
|---|---|
| trigger | What starts a run? An event or a command, not "when needed". |
| goal | What is true when the loop has succeeded? Someone can check it. |
| verification | Which command tells you? It exits with a non-zero status when the check is not met. |
| stopping rule | When does the loop stop? Because the work is done, and after a fixed number of passes anyway. |
| memory | Which file keeps the state between passes? |

## Where the five parts come from

The list is one author's definition. It comes from one position paper by Sandeco
Macedo (arXiv 2607.00038, https://arxiv.org/abs/2607.00038), titled:

"Stop Hand-Holding Your Coding Agent: Engineering the Loops that Replace Step-by-Step Prompting"

It is not a standard, and the second paper below does not use the name. The abstract calls
the object the loop specification: "a bounded, reusable artifact, made of a trigger, a
goal, a verification step, a stopping rule and a memory". This exercise uses the
abstract's list.

- Section 3 of the same paper lists a slightly different five: trigger, goal, an
  execution phase that calls named skills, verification and stopping rule. It adds
  memory separately: "A memory of progress and decisions persists
  across turns, on disk rather than in the conversation."
- The paper calls itself "a position paper anchored in a descriptive corpus study, not a
  controlled experiment". It draws no causal conclusion.
- A second paper looks at loops in public code: "Loop Engineering: Building Blocks,
  Adoption, and Impact", by Jai Lal Lulla, Vahram Nersesyan, Seyedmoein Mohsenimofidi,
  Christoph Treude and Sebastian Baltes (arXiv 2608.21884,
  https://arxiv.org/abs/2608.21884). It is under review. It does not use the term loop
  spec and has no five-part list. It names building blocks such as a trigger, a stop
  condition and durable state outside the context window, and its experiment on
  autonomy is planned, not run.
- Neither paper tests whether loops improve outcomes. The five parts are a way to write
  a loop down, not evidence that a loop written this way works better.

The checker in this folder is ours. It tests the shape of what you wrote. It cannot
show whether your goal is the right one or whether your command is a good test.

On the verification part, the first paper ranks checks from deterministic ones ("an
assertion, an exit code, a golden output") up to a model as judge and a human, and says
"do not pretend that level 4 is level 1". The checker accepts only the first kind, a
command with an exit status, because that is the kind it can see.

## What is in the folder

| File | Role |
|---|---|
| `spec_template.md` | The five sections with a TODO in each. Save a copy as `my_spec.md`. |
| `check_spec.py` | Grades a spec: all five fields present, and each one usable. |
| `samples/good.md` | A spec that passes, for the E17 loop. |
| `samples/vague.md` | A spec that fails in all five fields. |
| `samples/no_cap.md` | A spec with one field wrong: the stopping rule has no number. |
| `run_spec.py` | Reads a spec that passes and runs `exercises/e17/ralph.py` with the cap and the memory file from it. |

`run_spec.py` needs the whole `starter/` folder, because it calls `exercises/e17/ralph.py`
and that file needs `agent/`. It works in a temporary folder and deletes it at the end.

## Steps

Run every command from the `starter/` folder.

1. Check the three samples: `python3 exercises/e18/check_spec.py exercises/e18/samples`.
   Read the reason printed for each failed field. Which fields of `vague.md` fail, and
   what does `no_cap.md` lack?
2. Save a copy of `exercises/e18/spec_template.md` as `my_spec.md` in the `starter/`
   folder (with your editor, no command needed). Replace each TODO with a sentence or
   two about the E17 loop. Run `python3 exercises/e18/check_spec.py my_spec.md` after each
   edit until it prints PASS.
3. Run your spec: `python3 exercises/e18/run_spec.py my_spec.md`. Find the two lines of
   your spec that the script used, and the three it only showed.

Done when you can say: why "when needed", "looks good" and "the agent remembers" each
fail; why a stopping rule needs both a success condition and a number of passes (what
would the E17 loop have done without the number?); which command in your spec exits
non-zero when the goal is not met; and which two fields `run_spec.py` took from your
spec.

## Notes

- Python 3.10 or newer is needed (`python3 check_env.py`). No network, no key, no git
  in this exercise itself (the E17 loop it calls uses git in a temporary folder).
- `check_spec.py` exits 0 when every spec passes and 1 when a field fails. `run_spec.py`
  exits 0 when the loop finished every item, 1 when the cap stopped it with an item
  still open, and 2 when your spec fails the check or the memory file is not written.
  With the E17 plan the cap stops the loop, so exit 1 is the expected result.
- Try it for yourself: change the number of passes in your stopping rule to 2 and run
  step 3 again. Then name `notes.md` as the memory file and run it once more: the
  loop does not write that file, so the script stops with exit 2 and says so.
- The commands inside a spec name files of the E17 work folder (`test_items`,
  `fix_plan.md`). They are text for the loop, not lines to type in `starter/`.
- Delete `my_spec.md` when you finish. Nothing else is left behind.
- There is no `--live` option here. The loop it calls runs the scripted model only.
