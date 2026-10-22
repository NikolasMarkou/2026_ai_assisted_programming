# E21 Review an agent-made pull request: read it, check the claims, keep what you learn

Everything here is made by the course authors. No model runs, nothing is measured about
real agents, and nothing leaves your machine. The pull request in `agent_pr/` is a small
change that we wrote to look like an agent's work. It has one planted flaw. The two
scripts read files and print no banner. This folder uses only the standard library and
needs nothing from the other exercises.

## The pattern

An agent can produce a change, and a description of it, in seconds. Somebody still has
to know that the change works. Simon Willison, in his guide "Agentic Engineering
Patterns" (https://simonwillison.net/guides/agentic-engineering-patterns/, chapters read
on 2026-10-22; they change, so check the pages), writes about this in four chapters.
This exercise uses one idea from each.

| Chapter | What he says | Page |
|---|---|---|
| Writing code is cheap now | "Delivering new code has dropped in price to almost free... but delivering good code remains significantly more expensive than that." This chapter does not name review as a cost. The reviewer's side comes up in the Anti-patterns chapter. | .../code-is-cheap/ |
| Hoard things you know how to do | "A key asset to develop as a software professional is a deep collection of answers to questions like this, accompanied by proof of those answers." | .../hoard-things-you-know-how-to-do/ |
| Interactive explanations | "When we lose track of how code written by our agents works we take on cognitive debt." His remedy is to improve your understanding of the code, for example with an explanation the agent builds for you. | .../interactive-explanations/ |
| Anti-patterns | "Don't file pull requests with code you haven't reviewed yourself." The rule is about filing a pull request. He does not write a rule about merging. | .../anti-patterns/ |

Cognitive debt and the interactive explanation are his ideas. His companion chapter on
linear walkthroughs has the agent show code with shell commands: "sed or grep or cat or
whatever you need to include snippets of code you are talking about", so that it does not
copy code by hand. The walkthrough in this folder follows that idea on a tiny file. It is
our own small illustration. It is not his showboat tool.

All of this is one author's practice, with his own examples. The guide does not report a
measurement, and neither does this exercise.

## What is in the folder

| File | Role |
|---|---|
| `agent_pr/cart.py` | The small module after the change. It holds its own tests at the bottom. |
| `agent_pr/diff.patch` | The change: the module before and after, as a unified diff. |
| `agent_pr/pr_text.md` | The pull request text the agent wrote. It makes 3 claims. |
| `walkthrough.py` | Reads `cart.py` with Python versions of `wc -l`, `grep -n -E` and `sed -n`, and prints each command with what it returned. It holds no code typed by hand. |
| `check_claims.py` | Finds the claims that start with `tests`, `covers` or `fixes` in the text, and flags a claim that has no evidence. |
| `review_checklist.md` | Five points from Willison's pull request checklist, with a place for your answers. |
| `hoard.md` | One entry with its proof command, and a place for yours. |

## Steps

Run every command from the `starter/` folder.

1. Run the walkthrough: `python3 exercises/e21/walkthrough.py`. Read it from the top.
   Which lines in it are command lines, and which block shows where the discount is
   limited? Then read `agent_pr/pr_text.md` in your editor.
2. Check the claims: `python3 exercises/e21/check_claims.py exercises/e21/agent_pr`.
   Which claim is flagged, and what does the report say is missing? Look for the name in
   `agent_pr/diff.patch`.
3. Fill in `review_checklist.md` in your editor: yes or no and one line for each of the
   5 points, and your decision. Then read the proof command of Entry 1 in `hoard.md` and
   run it: `python3 exercises/e21/agent_pr/cart.py --discount 120 2000 500`. Write Entry
   2 in the same file about one thing you saw work today, with its own proof command, and
   run that command too.

Done when you can say: which claim has no evidence and what you would ask the author to
do; whether the change itself works (run `cart.py` with a discount of 120 and read the
output); which of the 5 points the description fails; what the walkthrough shows that
the diff alone does not; and what your hoard entry proves.

## Notes

- Python 3.10 or newer is needed (`python3 check_env.py`). No network, no key, no git.
- `check_claims.py` exits 0 when every claim has evidence, 1 when a claim is flagged and
  2 when a file cannot be read. `walkthrough.py` exits 0, or 2 when its file cannot be
  read. Exit 1 from `check_claims.py` is the expected result here.
- Evidence in `check_claims.py` means a test name that is defined in a changed file, or
  a command output pasted under a line that starts with `$ `. It reads the shape of the
  text. It does not run the pasted command, it does not run the tests, and it cannot
  see whether a test checks what the claim says. Run the tests yourself:
  `python3 -m unittest exercises/e21/agent_pr/cart.py`.
- Try for yourself: `walkthrough.py` takes any Python file, for example
  `python3 exercises/e21/walkthrough.py check_env.py`. Change a line of a copy of
  `cart.py` and run the walkthrough on the copy: the walkthrough changes with it.
- The walkthrough explains structure. It does not say whether the code is right. A
  walkthrough an agent writes can be wrong too, so check it against the file.
- There is no `--live` option here and no model call.
