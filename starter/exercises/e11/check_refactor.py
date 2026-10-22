"""Check a refactor of legacy.py: tests, public API and five structural measures.

    python3 check_refactor.py record   # BEFORE you edit: tests must be green
    python3 check_refactor.py          # AFTER the refactor

record saves the measures and the public function signatures of legacy.py in
legacy_baseline.json. The second command exits 1 when the tests fail, when a public
function is gone or has other parameters, or when no measure got smaller. Exit 2 means
no baseline (run record first). Standard library only.
"""
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

MODULE = Path("legacy.py")
BASELINE = Path("legacy_baseline.json")
WINDOW = 3  # a duplicated block is 3 equal consecutive code lines
PLAIN_NUMBERS = (0, 1)
LABELS = {"longest_function": "longest function (lines)",
          "duplicated_lines": "duplicated lines", "max_nesting": "deepest nesting",
          "magic_numbers": "number literals in code",
          "mutable_defaults": "mutable default arguments"}


def functions(tree):
    return [n for n in tree.body if isinstance(n, ast.FunctionDef)]


def nesting(node, depth=0):
    """Deepest chain of if, for, while, try and with blocks under node."""
    blocks = (ast.If, ast.For, ast.While, ast.Try, ast.With)
    deeper = depth + isinstance(node, blocks)
    return max([deeper] + [nesting(c, deeper) for c in ast.iter_child_nodes(node)])


def duplicated_lines(source):
    """Count code lines inside a 3-line window that occurs at least twice."""
    code = [(n, l.strip()) for n, l in enumerate(source.splitlines(), 1)
            if len(l.strip()) > 5 and not l.strip().startswith(("#", '"""'))]
    windows = {}
    for i in range(len(code) - WINDOW + 1):
        key = tuple(text for _, text in code[i:i + WINDOW])
        windows.setdefault(key, []).append(i)
    covered = {i + k for starts in windows.values() if len(starts) > 1
               for i in starts for k in range(WINDOW)}
    return len(covered)


def measures(source):
    """Return the five structural measures of a module as a dict of ints."""
    tree = ast.parse(source)
    funcs = functions(tree)
    numbers = [n for f in funcs for n in ast.walk(f) if isinstance(n, ast.Constant)
               and isinstance(n.value, (int, float)) and not isinstance(n.value, bool)
               and n.value not in PLAIN_NUMBERS]
    mutable = [d for f in funcs for d in f.args.defaults + f.args.kw_defaults
               if isinstance(d, (ast.List, ast.Dict, ast.Set))]
    return {"longest_function": max(f.end_lineno - f.lineno + 1 for f in funcs),
            "duplicated_lines": duplicated_lines(source),
            "max_nesting": max(nesting(f) for f in funcs),
            "magic_numbers": len(numbers), "mutable_defaults": len(mutable)}


def public_api(source):
    """Map each public function name to its parameters as (name, has_default)."""
    api = {}
    for f in functions(ast.parse(source)):
        if not f.name.startswith("_"):
            a = f.args
            plain = a.posonlyargs + a.args
            flags = [i >= len(plain) - len(a.defaults) for i in range(len(plain))]
            api[f.name] = [[p.arg, d] for p, d in zip(plain, flags)] + [
                [p.arg, d is not None] for p, d in zip(a.kwonlyargs, a.kw_defaults)]
    return api


def run_tests():
    done = subprocess.run([sys.executable, "-m", "unittest", "-q"],
                          capture_output=True, text=True)
    ran = re.search(r"^Ran (\d+) test", done.stderr, re.M)
    return done.returncode == 0, int(ran.group(1)) if ran else 0


def record():
    ok, ran = run_tests()
    print(f"tests: {ran} run, {'all pass' if ok else 'FAILING'}")
    if not ok:
        print("RESULT: tests must be green before you start")
        return 1
    source = MODULE.read_text(encoding="utf-8")
    BASELINE.write_text(json.dumps({"measures": measures(source),
                                    "api": public_api(source)}, indent=2) + "\n")
    print(f"recorded {BASELINE}: {len(public_api(source))} public functions")
    return 0


def api_problems(before, now):
    """Messages for each public function that is gone or has other parameters."""
    return [f"public function changed or gone: {name}"
            for name, params in before.items() if now.get(name) != params]


def print_measures(before, after):
    """Print the before and after table. Returns the keys that got smaller."""
    print(f"{'measure':28}{'before':>8}{'after':>8}")
    smaller = []
    for key, label in LABELS.items():
        old, new = before[key], after[key]
        word = "smaller" if new < old else "same" if new == old else "LARGER"
        smaller += [key] if new < old else []
        print(f"{label:28}{old:>8}{new:>8}  {word}")
    return smaller


def check():
    if not BASELINE.exists():
        print("RESULT: no baseline. Run `python3 check_refactor.py record` first.")
        return 2
    before = json.loads(BASELINE.read_text())
    source = MODULE.read_text(encoding="utf-8")
    after, api = measures(source), public_api(source)
    ok, ran = run_tests()
    print(f"tests: {ran} run, {'all pass' if ok else 'FAILING'}")
    problems = ([] if ok else ["tests fail"]) + api_problems(before["api"], api)
    print(f"public functions: {len(before['api'])} before, "
          f"{len(before['api']) - len(api_problems(before['api'], api))} unchanged")
    smaller = print_measures(before["measures"], after)
    if not smaller:
        problems.append("no measure got smaller: nothing was refactored")
    for extra in sorted(set(api) - set(before["api"])):
        print(f"NOTE: new public function {extra}; start helper names with _")
    if len(smaller) > 1:
        print(f"NOTE: {len(smaller)} measures got smaller. "
              "Was the diff only the top smell?")
    print("RESULT: " + ("PASS" if not problems else "FAIL: " + "; ".join(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(record() if sys.argv[1:] == ["record"] else check())
