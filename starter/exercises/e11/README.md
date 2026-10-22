# E11 Smells, refactor, document

`legacy.py` is an order module of about 100 lines that works and has never been cleaned up.
`tests/test_legacy.py` pins what it does today, right or wrong, with a table of inputs and the outputs they
give. The tests pass. Your job is to improve one thing in it and prove that nothing else changed.

Run the tests from this folder:

```text
python3 -m unittest -q
```

## Steps

1. Record the starting point. This runs the tests and saves 5 measures of `legacy.py`:

   ```text
   python3 check_refactor.py record
   ```

2. Ask your agent to list the code smells in `legacy.py`, ranked by severity and by fix
   effort. Read the list and decide yourself which smell is the top one. Write down the
   ranking before you continue.
3. Fix only the top smell. Keep every public function name and parameter list. Run the
   tests after the change.
4. Run the check. It runs the tests, compares the public functions with step 1 and
   prints each measure before and after:

   ```text
   python3 check_refactor.py
   ```

5. Ask your agent to write a README section for the module. Save it as `README_section.md`
   and check it against the code:

   ```text
   python3 check_readme.py legacy.py README_section.md
   ```

   The check fails when the README names a function that does not exist (written as
   `name()` in backticks) or when a public function is not mentioned. Read the README
   yourself too: the check cannot see a wrong sentence.

Done when the tests pass before and after, `check_refactor.py` prints PASS, the diff holds
only the one refactor, and `check_readme.py` prints PASS.
