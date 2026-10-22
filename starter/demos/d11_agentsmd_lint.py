"""Demo 11: AGENTS.md goes stale like any list of dependencies.

Writes a sample repository to a temporary directory, with a Makefile that has a
test target and no verify target, and runs the lint from exercises/e5 on its
AGENTS.md. Standard library only.
"""
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises" / "e5"))
import lint_agents_md  # noqa: E402

SAMPLE = """# Project: invoice-service
- Test: `python3 -m unittest -q`
- Status: `git status --short`
- Check: `make test`
- Never edit files under `migrations/` by hand. Docs live in `docs/`.
- Run `make verify` before you finish.
"""
workdir = tempfile.TemporaryDirectory()
repo = Path(workdir.name)
(repo / "AGENTS.md").write_text(SAMPLE)
(repo / "Makefile").write_text("test:\n\t@echo tests would run here\n")
(repo / "docs").mkdir()

exit_code = lint_agents_md.main([str(repo / "AGENTS.md")])
print("exit code:", exit_code)

# Hidden check (not shown)
found = lint_agents_md.lint(SAMPLE, repo)
assert [s for s, _, _ in found].count("ok") == 4
assert sorted(d for s, _, d in found if s == "GONE") == ["make verify", "migrations/"]
assert exit_code == 1
workdir.cleanup()
