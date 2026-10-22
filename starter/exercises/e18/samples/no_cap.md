# Loop spec: fix the items of fix_plan.md, without a cap

## trigger
A person types `python3 exercises/e17/ralph.py` in the starter folder.

## goal
Every item in fix_plan.md is ticked and the tests in test_items.py pass.

## verification
`python3 -m unittest -q test_items` in the work folder. The command exits with a
non-zero status when a test fails.

## stopping rule
Stop when no unchecked item is left in fix_plan.md.

## memory
`progress.md` in the work folder, one line per pass.
