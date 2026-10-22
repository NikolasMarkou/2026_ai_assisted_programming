# E14 answer key: the 6 scenarios

Labels allowed: `use AI`, `use with heavy review`, `avoid`. Scenarios 1 to 6 differ in how firm the key is: 5 of them have a
defensible second label; the reason a pair gives matters more than the label. Accept the
alternative in the last column when the reason names the right risk.

| # | Scenario | Key | Reason | Accepted alternative |
|---|---|---|---|---|
| 1 | CSV report parser | use AI | Low blast radius, and the output can be checked against the input by a person or a test. | none |
| 2 | JWT validation middleware | use with heavy review | Auth is security-critical logic (first cut 10.5). A mistake passes tests and fails only against an attacker. Prefer a maintained library and have a person with security skill review every line. | avoid, if the team has no such reviewer |
| 3 | Migration that drops columns | use with heavy review | Data deletion and migrations are human checkpoints (first cut 7.2). The agent drafts the migration and the rollback; a person checks both on a copy of the data and approves. It cannot be undone once it is applied. | avoid for the apply step |
| 4 | Learning an unfamiliar library | avoid | Delegating the code removes the practice that builds understanding. In Anthropic's trial (52 mostly junior engineers learning a library, 2026-01-29) the AI group scored 50% on the comprehension quiz against 67% for hand coding (C-062, n=52, one study). Use the agent to explain, and write the code yourself. | use with heavy review, if the pair says they will read and re-type it |
| 5 | Medical device dose calculation | avoid | A regulated domain where each line must be explained and certified (first cut 10.5). A person writes and certifies the calculation. The agent can help with tests, documentation and a review checklist, which a person still checks. | use with heavy review for tests only |
| 6 | Novel scheduling algorithm | avoid | With no reference solution, a plausible wrong answer cannot be told from a right one (first cut 10.5: novel algorithm design has few patterns to draw from). Write a brute-force checker first; the agent may write the checker and the tests. | use with heavy review, if a brute-force checker exists first |

## Settings table

There is no key: the answer is what the pair finds in their own tool today. Check that
each row has a date and an actual value; "default" is not a value. Retention, training and indemnity
terms differ by plan and change; this deck makes no claim about any vendor's current
terms. If a pair cannot find a setting, they write that on the sheet and do not guess.

## For the discussion

- Ask pairs that labelled #2 "use AI" what test would detect a token the middleware wrongly
  accepts. If a pair has no such test, that is the finding.
- Item #4 is the one the trainer has a story for: a greenfield project the trainer never
  read, a mess by week 6 (n=1, the trainer's own). Say it is n=1.
- IP: in the US the Supreme Court denied review on 2026-03-02, leaving the rule that
  AI-only work has no copyright (C-076, REVERIFY). Other jurisdictions are not covered.
