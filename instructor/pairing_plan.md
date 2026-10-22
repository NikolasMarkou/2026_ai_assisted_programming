# Pairing plan

Goal: every pair holds 2 different tools, so that each exercise gives 2 results for one
task. The sign-in sheet decides who can pair with whom.

## Before 09:00: build the sheet

1. At the door, each person writes name, tool (Cursor, Codex, Claude Code or OpenCode),
   whether it is signed in, and whether they have a usage budget. One row per person.
2. Run `python3 check_env.py` on any laptop that is not working. Move that person to the
   spare machine before E3.
3. Count the tools. The pairs are made from the largest group down.

## Making the pairs

1. Sort the people by tool. Take the person from the largest tool group and pair them with
   a person from the next largest group. Repeat until one group is empty.
2. If people are left, they all use the same tool. Pair them by a different model or a
   different configuration (next section).
3. An odd number gives one group of 3. In the group of 3 two people share a laptop for
   E3 and E10 and the third reviews; rotate the roles each exercise.
4. Write each pair on the shared sheet: pair number, both names, both tools. The sheet
   columns for results are `pair, tool, exercise, time, result, note`
   (`instructor/results_sheet_template.csv`).

## When everyone uses the same tool

Different models, same tool: each person picks a different model in the tool's model
menu and writes the model name on the sheet. Different configuration, same model: one
person runs with the instruction file `AGENTS.md` from E5 and one without it, or one in
plan mode and one not. For E10 each pair keeps its own block of 5 seeds
(`--seeds 1-5` for the first pair, `6-10` for the next, and so on) so that the pairs add up
to a larger sample.

## What each pair does with the second tool

- E2, E4: swap one prompt and run it in the partner's tool.
- E3: each person runs the minimal agent trace on their own laptop; compare the labels.
- E8, E9: the partner runs the review of the fix, in their own tool.
- E10: each person runs the harness with their own agent command; compare the spread.
- E11 to E13: one person drives, the other reads the diff and the commands before they run.
- E14: classify alone, then compare the 6 labels and discuss the ones that differ.

## Rotation for E15 (capstone)

Pairs are re-made for the capstone so that nobody reviews a feature they built.

1. Each person picks 1 of the 4 backlog features and builds it alone, in their own tool.
2. At the review step, each person gives the diff to a person from another pair, who
   reads it, runs the tests and fills the checklist question "what did you verify?".
3. Rotation rule: person number n reviews person number n+1 on the sheet; the last
   person reviews the first. If n+1 chose the same feature, move to n+2.
4. The author fixes what the reviewer found, then runs `check_capstone.py` and
   adds the output of `git log main..feature` and `git diff main feature` to
   `PR_DESCRIPTION.md` and copies it, with `bookmarks.py`, to a folder of their own in
   the pair's subfolder of the exchange folder. The reviewer's name goes on the description.
5. Collect the 4-part checklist (model, harness, sandbox, knowledge and tools) from each
   `PR_DESCRIPTION.md` for the close.

## If a pair falls apart

A person leaves, or a tool fails: merge them into the nearest pair as a third. Never
leave a person alone with a failed tool; they use the scripted agent
(`python3 agent/minimal_agent.py DIRECTORY`) for E3, E8 and E10 and a partner's tool for the rest.
