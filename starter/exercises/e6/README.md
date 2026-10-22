# E6 Scaffold and complete

Files in this folder:

- `spec.md`: the spec for a notes service (part 1) and for one function (part 2).
- `check_scaffold.py`: starts your service on a free port, tests the 4 endpoints and checks
  imports.
- `duration.py`: the function stub with its docstring and 3 examples.

## Steps

1. Work in a copy: `cp -r exercises/e6 e6_work` (run from `starter/`).
2. Give your agent `spec.md`, part 1. Ask for `service.py` in `e6_work`. Before it writes any
   code, ask which files it will create and which packages it will import.
3. Run `python3 exercises/e6/check_scaffold.py e6_work`. Read the failing line, fix, run again.
4. Part 2: ask the agent to implement `parse_duration` in `e6_work/duration.py`. It may not
   change the docstring. Run `python3 -m doctest duration.py` inside `e6_work`.
5. Look at the imports of everything the agent wrote. Any import outside the standard
   library is a dependency you did not approve.

Done when `check_scaffold.py` prints 4 of 4 endpoints pass and the doctests print nothing.
