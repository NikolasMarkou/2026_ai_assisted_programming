# E20 Parallel agents in git worktrees: pick, merge, and what a worktree does not do

Everything here is scripted by the course authors. No model runs, nothing is measured
about real agents, and nothing leaves your machine. Every demo output starts with the
line `SCRIPTED DEMONSTRATION by the course authors, not a measurement`. There is no
`--live` option in this folder. `same_file_check.py` is a tool for your own
repositories, so it prints no banner.

## The pattern

A git worktree is a second folder of files for the same repository. Two agents can each
work in their own worktree, on their own branch, at the same time. The git manual
(https://git-scm.com/docs/git-worktree) says "A git repository can support multiple
working trees, allowing you to check out more than one branch at a time." A branch can
be checked out in one worktree only. Git refuses a second one unless you force it with
`--force`. Codex's documentation gives the same rule: "Git only allows a branch to be
checked out in one place at a time."

What three tools document (pages read on 2026-10-22; vendor pages change, so check them
before you rely on a detail):

| Tool | What its page says | Page |
|---|---|---|
| Claude Code | `claude --worktree <name>` makes a checkout under `.claude/worktrees/<name>/` on a new branch `worktree-<name>` | https://code.claude.com/docs/en/worktrees.md |
| Codex | Worktrees start on a detached HEAD, so several of them do not add branches | https://learn.chatgpt.com/docs/environments/git-worktrees.md |
| Cursor | `/best-of-n` "runs the same task across multiple models at once. Each run gets its own worktree" | https://cursor.com/docs/configuration/worktrees.md |

Best-of-N is a Cursor feature. The same page says it "compares runs only. It does not
merge changes back into your main checkout for you." So you look at the results, you
pick the winner, and nothing is merged back. The Claude Code and Codex pages we read do
not describe best-of-N. Do not attribute it to them.

No vendor page that we read documents a merge order, or says what happens when two
agents edit the same file. The same-file check and the merge-order advice in this
exercise are the course's own, not a vendor procedure.

A worktree is not a sandbox. The Claude Code page says edits and git commands aimed at
the main checkout are blocked, and also says "a command that writes into the main
checkout without running git there, such as `cp` or a shell redirect, isn't refused".
`not_a_sandbox.py` shows the same thing with our own scripted agent and plain git. It
does not test any vendor tool. The sandbox is one of the 4 parts of an agent, and a
later exercise covers it.

## What is in the folder

| File | Role |
|---|---|
| `worktree_demo.py` | `best`: two agents solve one task in two worktrees, you pick, nothing is merged back. `merge`: three pairs of agents on two tasks each; same-file check, then a merge in each order with the tests run after every merge. |
| `agents.py` | The scripted agents: fixed edits to files in a worktree, and one handoff line each. |
| `same_file_check.py` | Lists the files each branch touched and flags a file that two branches touched. Works on your own repository. |
| `not_a_sandbox.py` | Our own run: a scripted agent in one worktree writes into the main checkout by path, and a branch made in one worktree is visible from the main checkout. |
| `task_repo.py` | The shared helper: temporary repository, worktree, merge and test runner. It sets a git identity and dates itself. |

Each script builds its repositories in a temporary folder and deletes them at the end.
The output has no path and no hash, so it is the same on every machine.

## Steps

Run every command from the `starter/` folder.

1. Run the best-of-N demo: `python3 exercises/e20/worktree_demo.py best`. Read the two
   result lines. Which agent would you pick, and what is main's state after the pick?
2. Run the merge-order demo: `python3 exercises/e20/worktree_demo.py merge`. For each of
   the 3 pairs read the same-file line, then the two merge orders. Which pair does the
   same-file check flag, and which pair has a clean merge whose tests fail?
3. Run the sandbox demo: `python3 exercises/e20/not_a_sandbox.py`. Find the two lines of
   `git status` in the main checkout that the agent caused.

Done when you can say: why the pick leaves main where it was; what git reports for pair 2
and when; why the same-file check says nothing for pair 3 although the merged result
fails; which merge turns the tests red in each order for pair 3; and what a worktree
separates and what it does not.

## Notes

- Python 3.10 or newer and git 2.5 or newer (the first version with `git worktree`).
  `python3 check_env.py` prints your git version. No network, no key. You do not need to
  set a git identity: the scripts pass their own, and they never touch your own
  repositories. On Windows use WSL2 or Git Bash, because the sandbox demo runs shell
  commands.
- Try for yourself: `worktree_demo.py best --pick b` (you pick the other result),
  `worktree_demo.py best --apply` (you merge the pick into main yourself, then the tests
  run in main), and `python3 exercises/e20/same_file_check.py . main branch-a branch-b`
  in a repository of your own.
- The agents are fixed scripts. Real agents would not produce these exact edits, and
  nothing here says how often real agents touch the same file.
- A clean merge does not mean working code. Git compares text. Only the tests run on the
  merged result see that one branch broke what the other uses.
- A vendor that sells preview environments (Upsun) writes that port conflicts hit first
  and that worktrees share the same local database
  (https://developer.upsun.com/posts/ai/git-worktrees-for-parallel-ai-coding-agents).
  That is the vendor's statement. This exercise does not test it.
