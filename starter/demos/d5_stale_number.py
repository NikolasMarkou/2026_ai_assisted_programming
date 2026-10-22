"""Demo 5: the agent changes a value; the checker reads only the files it was
built to read. Standard library only.
"""
import re
import tempfile
from pathlib import Path

workdir = tempfile.TemporaryDirectory()
root = Path(workdir.name)
files = {
    "app/config.py": "REQUEST_TIMEOUT_S = 30   # agent changed this from 10\n",
    "tests/test_config.py": "from app.config import REQUEST_TIMEOUT_S\n"
                            "assert REQUEST_TIMEOUT_S == 30\n",
    "README.md": "Requests time out after 10 seconds.\n",
    "deploy/service.yaml": 'env:\n  - name: REQUEST_TIMEOUT_S\n    value: "10"\n',
    "docs/runbook.md": "A call longer than 10 s is killed; page the on-call at 10 s.\n",
    "AGENTS.md": "Never set the request timeout above 10 s.\n",
}
for name, text in files.items():
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)

# The checker reads the code and the tests, as every unit-test run does.
checked = list(root.rglob("*.py"))
print(f"checker read {len(checked)} files, found 0 problems  -> GREEN")

# The sweep searches the OLD value in every file, whatever its type.
old = re.compile(r"\b10\b")
hits = [(path.relative_to(root), n, line.strip())
        for path in sorted(root.rglob("*")) if path.is_file()
        for n, line in enumerate(path.read_text().splitlines(), 1)
        if old.search(line)]
print(f"sweep for the old value 10 in all {len(files)} files -> {len(hits)} hits")
for path, n, line in hits:
    print(f"  {path}:{n}  {line}")

# Hidden check (not shown)
assert len(checked) == 2 and len(files) == 6 and len(hits) == 5
assert [str(h[0]) for h in hits] == ["AGENTS.md", "README.md", "app/config.py",
                                     "deploy/service.yaml", "docs/runbook.md"]
workdir.cleanup()
