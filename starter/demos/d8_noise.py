"""Demo 8: the class mini eval (3 tasks x 2 trials) when the AGENTS.md rule does
NOTHING. Both configurations pass each run with probability 0.6.
Standard library only.
"""
import random

random.seed(7)
P_PASS = 0.6
EVALS = 20000


def resolve_rate(tasks, trials):
    """Share of passing runs in one eval of tasks x trials runs."""
    runs = sum(random.random() < P_PASS for _ in range(tasks * trials))
    return runs / (tasks * trials)


print(f"each run passes with probability {P_PASS} in both; the rule does nothing")
results = []
for tasks, trials in [(3, 2), (10, 3), (30, 5)]:
    ahead = gap = 0
    for _ in range(EVALS):
        a, b = resolve_rate(tasks, trials), resolve_rate(tasks, trials)
        ahead += b > a + 1e-9
        gap += abs(b - a) >= 0.15
    results.append((ahead, gap))
    print(f"{tasks:>2} tasks x {trials} trials: gap of 15+ points in "
          f"{gap / EVALS:4.0%} of evals, 'rule' ahead in {ahead / EVALS:4.0%}")

# Hidden check (not shown)
assert results == [(7770, 15528), (8965, 4691), (9510, 161)]
