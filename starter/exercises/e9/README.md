# E9 Diagnose and guard

`report.py` builds a nightly sensor report. `trace.txt` is the log of the night it
crashed. `nightly.py` (the job that calls it) is not part of this kit. The tests in
`tests/` all pass.

Run the tests from this folder:

```text
python3 -m unittest -q
```

## Steps

1. Paste `trace.txt` into your agent. Ask for the root cause, a minimal reproduction and a fix.
   Do not paste `report.py` yet: note what it asks for.
2. Run the reproduction yourself. Apply the fix.
3. Ask the agent to review `git diff` (or the changed file) and list the tests that should be
   added or changed. Look at `test_a_night_with_no_readings` before you accept the list.
4. Add a regression test. Revert the fix, run the tests, and confirm the new test fails.
   Put the fix back and confirm all tests pass.
5. If the agent got any step wrong, label that failure with `diagnostic.md`.

Done when the fix has a regression test that fails without the fix.
