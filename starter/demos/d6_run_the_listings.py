"""Demo 6: every code listing parses. Run the listings and read the results.

Five snippets in the style an assistant writes with confidence.
Standard library only.
"""
import ast

LISTINGS = {
    "range with a dtype": 'xs = list(range(3, "int"))\n',
    "load json from a path": 'import json\ndata = json.loads("config.json")\n',
    "join two paths": ('import os\n# absolute path stays inside /srv/data\n'
                       'p = os.path.join("/srv/data", "/etc/passwd")\n'
                       'assert p.startswith("/srv/data"), p\n'),
    "round half up": ("# rounds .5 up, like school\n"
                      "assert round(2.5) == 3 and round(0.5) == 1, "
                      "(round(2.5), round(0.5))\n"),
    "this one is fine": 'print(sorted({"b": 2, "a": 1}))\n',
}
print(f"all {len(LISTINGS)} listings parse (ast.parse). Executed:")
verdicts = []
for name, src in LISTINGS.items():
    ast.parse(src)  # the build check: always passes
    try:
        exec(compile(src, name, "exec"), {})
        verdict = "runs and its own claims hold"
    except Exception as error:
        verdict = f"{type(error).__name__}: {error}"[:60]
    verdicts.append(verdict)
    print(f"{name:22} -> {verdict}")

# Hidden check (not shown)
assert verdicts == [
    "TypeError: 'str' object cannot be interpreted as an integer",
    "JSONDecodeError: Expecting value: line 1 column 1 (char 0)",
    "AssertionError: /etc/passwd",
    "AssertionError: (2, 0)",
    "runs and its own claims hold",
]
