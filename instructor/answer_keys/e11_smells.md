# E11 answer key: the planted smells in legacy.py

Intended top smell: **1, the long function `process_orders`**. Accept another top smell
if the pair argues it with a severity and an effort reason; check_refactor.py passes any
refactor that makes one measure smaller and keeps the tests and the public functions.

| Rank | Smell | Where | Severity | Fix effort | check_refactor measure |
|---|---|---|---|---|---|
| 1 | One long function doing 5 jobs: validate, price items, discount, tax and shipping, format | `process_orders` | High: every change touches it, it cannot be tested in parts | Medium: extract 3 helpers, same lines out | longest function 56 lines |
| 2 | Deep nesting, 7 levels of if and for | `process_orders` | High: hard to read, errors hide in the else branches | Low to medium: it falls when smell 1 is fixed | deepest nesting 7 |
| 3 | Duplicated block: the 3 lines that turn cents into text, copied 3 times | `process_orders` (twice), `summary` | Medium: a rounding fix must be made 3 times | Low: one `format_money()` function | duplicated lines 13 |
| 4 | Unnamed number literals: 19, 20, 15, 10, 5, 5000, 499, 700, 999 in the code | `process_orders`, `quote_shipping` | Medium: no name says what 499 is | Low: module constants | number literals 20 |
| 5 | Mutable default argument `coupons=[]` | `process_orders` | Low today (never changed inside), high if someone appends | Very low: `coupons=None` | mutable default arguments 1 |
| 6 | Misleading name: `check_country` returns a tax rate and checks nothing | `check_country` | Low to medium: callers guess wrong | Low, but renaming changes a public name and fails check_refactor | none |

Notes for the room:

- Severity and effort are judgements. A pair that ranks the duplication first because it is
  the cheapest fix with a real payoff has a defensible answer; check_refactor accepts it.
- Smell 6 is a trap for the check: renaming `check_country` removes a public name, so
  check_refactor FAILS with "public function changed or gone". That is intended: a rename
  of a public function is not a behaviour-preserving refactor of the module.
- Smell 5 is a latent defect: the list is only read today. The tests cannot see it, which
  is why it ranks low.
- The reference refactor is `instructor/solutions/e11/legacy.py` with the README section
  `README_section.md` in the same folder. It extracts `_price_items`, `_discount` and
  `_bill_order`, so the longest function falls from 56 to 24 lines and the nesting from 7
  to 4. It leaves smells 3 to 6 alone on purpose.
- The agent's README: look for a sentence the check cannot catch. Typical errors are a
  wrong tax rate, "raises an error" where the code returns -1, and a missing mode.
