"""Demo 9: the summary says healthy; the third row says otherwise.
Standard library only.
"""
import re

rows = ["case-%02d PASS" % i for i in range(1, 41)]
rows[2] = "case-03 SKIPPED (exception: KeyError 'balance' swallowed by retry wrapper)"
log = "\n".join(rows)

# The agent's check, written once and trusted for nine days.
failed = len(re.findall(r"\bFAIL(ED)?\b", log))
summary = f"{len(rows)} cases, {failed} failed. Pipeline healthy."
print("agent summary :", summary)

# The raw pass: read every row that is not PASS, with no metric and no hypothesis.
print("raw rows that are not PASS:")
odd = [row for row in rows if not row.endswith("PASS")]
for row in odd:
    print("  ", row)

# Hidden check (not shown)
assert summary == "40 cases, 0 failed. Pipeline healthy."
assert odd == [rows[2]]
