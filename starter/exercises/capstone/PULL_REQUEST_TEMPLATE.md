# Pull request description

Copy this file to `PR_DESCRIPTION.md`, replace every line that starts with `TODO`, and
keep the headings. `check_capstone.py` checks that no part is empty.

## The feature

TODO: the backlog item and the acceptance criteria you tested.

## The four parts of the agent that did the work

### model

TODO: which model and which version did the work? One line per model if you used more
than one (for example one for the code and one for the review).

### harness

TODO: what ran the checks (you, a hook, a script, the agent itself) and what retry cap
applied? Say where the agent had to stop and show you.

### sandbox

TODO: what was the agent allowed to touch (folders, network, branch, credentials)? Say
what you denied.

### knowledge and tools

TODO: which instruction files, skills, MCP servers or docs did the agent have?

## What the AI did

TODO: 2 to 4 sentences. Which files it changed and which steps it took on its own.

## What I verified

List at least 3 checks that you ran or read yourself, one per line, each starting with
`- `. Say what you saw. Do not copy what the agent told you.

- TODO: for example "ran python3 -m unittest -q: 12 tests, 0 failures"
- TODO: for example "read the whole diff: 2 files, no change outside bookmarks.py"
- TODO: for example "ran the new test on the old code and it failed"
