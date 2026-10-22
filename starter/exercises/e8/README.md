# E8 Lab: two bugs in a function of about 30 lines

`shipping.py` holds one function, `shipping_cents`. It has exactly 2 bugs. The visible
tests in `tests/` pass. The rules are in words in `spec.md`; 3 worked examples are in
`spec_examples.md`.

Run the visible tests from this folder:

```text
python3 -m unittest -q
```

## Steps

1. Give your agent `spec.md` and `spec_examples.md`. Ask it to write tests from the spec
   and the examples, before it reads `shipping.py`. Save them as `tests/test_spec.py`.
2. Run the tests. Each failing test belongs to one rule of the spec. Find the 2 bugs.
3. Fix both bugs with the smallest change that works. Do not edit the tests to make them pass.
4. Optional contrast, after the fix: copy the original `shipping.py` back, ask the agent to write tests from
   the code alone, and run them. Count how many tests pass on the buggy code.
5. Ask the instructor to run the hidden tests on your folder.

Done when both bugs are fixed and the hidden tests pass.
