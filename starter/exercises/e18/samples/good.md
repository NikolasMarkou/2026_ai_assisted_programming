# Loop spec: fix the items of fix_plan.md

## trigger
A person types `python3 exercises/e17/ralph.py` in the starter folder. In a team the
same loop could start on every push to the main branch.

## goal
Every item in fix_plan.md is ticked and the tests in test_items.py pass.

## verification
`python3 -m unittest -q test_items` in the work folder. The command exits with a
non-zero status when a test fails. An item is ticked only after the test class named on
that item has passed.

## stopping rule
Stop when no unchecked item is left in fix_plan.md. Also stop after 4 passes even if an
item is still open, and report the items that are open.

## memory
`progress.md` in the work folder, one line per pass, and fix_plan.md with its ticks.
