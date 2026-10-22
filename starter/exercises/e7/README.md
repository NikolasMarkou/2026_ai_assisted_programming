# E7 TDD and coverage

`pricing.py` is a stub that raises `NotImplementedError`. The rules are in `spec.md`.
There are no tests yet. `tests/` is an empty package, so `python3 -m unittest -q`
finds them when you add `tests/test_pricing.py`.

Tools in this folder (standard library only):

- `cov.py`: line coverage of one module, with the numbers of the lines no test ran.
- `check_untouched.py`: proves the recorded test files were not edited afterwards.

## Steps

1. Ask the agent for tests only, from `spec.md`, in `tests/test_pricing.py`. Do not let it
   write `pricing.py`. Run `python3 -m unittest -q` and confirm the tests fail.
2. Save the tests. Then record their hashes:
   `python3 check_untouched.py record tests`
3. Ask the agent for the implementation. Tell it not to touch the tests. Run the tests.
4. Run `python3 cov.py pricing.py --min 90`. Read the uncovered line numbers. Ask the agent
   for new tests (new test methods or a new file) that run those lines, and run again.
5. Run `python3 check_untouched.py check tests`. It lists any edited or deleted test file.

`cov.py` measures line coverage: a line counts when it ran at least once. It does not
record which side of an `if` ran. The real tool for that is optional:
`coverage run --branch -m unittest` and then `coverage report -m`.

Done when the tests pass, `cov.py` reports at least 90 percent, and `check_untouched.py`
reports no edited test.
