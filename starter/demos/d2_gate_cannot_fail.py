"""Demo 2: a green test suite that cannot fail.

The tests are written from the code's own output. Then we change the code one
comparison at a time and count how many changed versions the suite catches.
Standard library only.
"""
import ast

SRC = '''
def discount(total, years):
    """10% off from 100 EUR; loyal customers (5+ years) get 15%."""
    if total > 100:            # BUG 1: the spec says 100 or more
        rate = 0.10
    else:
        rate = 0.0
    if years > 5:              # BUG 2: the spec says 5 or more
        rate = 0.15
    return round(total * (1 - rate), 2)
'''


def load(src):
    namespace = {}
    exec(compile(src, "m", "exec"), namespace)
    return namespace["discount"]


buggy = load(SRC)
# Tests written by the agent: call the code, paste what it returned.
inputs = [(50, 1), (150, 1), (150, 9), (80, 9)]
agent_tests = [(i, buggy(*i)) for i in inputs]
# Tests written from the spec and never shown to the agent.
spec_tests = [((100, 1), 90.0), ((100, 5), 85.0), ((50, 5), 42.5)]


def score(fn, tests):
    return sum(fn(*i) == want for i, want in tests), len(tests)


print("agent tests on buggy code :", "%d/%d green" % score(buggy, agent_tests))
print("spec tests on the same    :", "%d/%d green" % score(buggy, spec_tests))


class FlipComparison(ast.NodeTransformer):
    """Flip the target-th comparison between > and >=."""

    def __init__(self, target):
        self.target, self.seen = target, 0

    def visit_Compare(self, node):
        if self.seen == self.target:
            flipped = ast.GtE() if isinstance(node.ops[0], ast.Gt) else ast.Gt()
            node.ops = [flipped]
        self.seen += 1
        return node


def changed_versions():
    for k in range(2):
        tree = FlipComparison(k).visit(ast.parse(SRC))
        ast.fix_missing_locations(tree)
        yield load(ast.unparse(tree))


caught = sum(score(m, agent_tests)[0] != len(agent_tests) for m in changed_versions())
print("changed versions the agent tests catch: %d of 2" % caught)

# Hidden check (not shown)
assert score(buggy, agent_tests) == (4, 4)
assert score(buggy, spec_tests) == (0, 3)
assert caught == 0
fixed = load(SRC.replace("total > 100", "total >= 100")
             .replace("years > 5", "years >= 5"))
assert score(fixed, spec_tests) == (3, 3)  # the spec tests can pass on correct code
assert score(fixed, agent_tests) == (4, 4)  # same result on fixed and buggy code
