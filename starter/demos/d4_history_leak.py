"""Demo 4: the eval clones the repo and checks out the base commit, but the fix
commit is still inside .git, where the agent can read it.

Needs git. Both repositories live in a temporary directory that is removed at
the end. Standard library otherwise.
"""
import subprocess
import tempfile
from pathlib import Path

GIT = "git -c user.name=x -c user.email=x@x"
root = tempfile.TemporaryDirectory()


def sh(command, cwd):
    r = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip()


def indent(text, pad="   "):
    return text.replace("\n", "\n" + pad)


upstream = Path(root.name) / "upstream"
upstream.mkdir()
(upstream / "dates.py").write_text("def year(s):\n    return int(s[:3])\n")
sh(f"git init -q -b main && git add -A && {GIT} commit -qm base", upstream)
base = sh("git rev-parse HEAD", upstream)
(upstream / "dates.py").write_text("def year(s):\n    return int(s[:4])\n")
sh(f"{GIT} commit -qam 'fix: year slice is 4 characters'", upstream)

trial = Path(root.name) / "trial"  # what a first-cut harness does:
sh(f"git clone -q {upstream} {trial}", root.name)  # clone, then check out the base
sh(f"git checkout -q {base}", trial)
print("working tree is at the base commit:\n  ", indent(sh("cat dates.py", trial)))
leaked = sh("git log --all --format=%s", trial)
print("what the agent can still run:")
print("  $ git log --all --format=%s\n  ", indent(leaked))
diff = sh("git diff HEAD origin/main -- dates.py | tail -4", trial)
print("  $ git diff HEAD origin/main\n  ", indent(diff))
# Fix: drop every ref except the base and prune, or copy the tree without .git.
sh(f"git checkout -q -b eval {base} && git branch -D main -q"
   " && git remote remove origin && git reflog expire --expire=now --all"
   " && git gc -q --prune=now", trial)
after = sh("git log --all --format=%s", trial)
print("after removing the remote and pruning:\n  ", after)

# Hidden check (not shown)
assert leaked == "fix: year slice is 4 characters\nbase"
assert "+    return int(s[:4])" in diff
assert after == "base"
root.cleanup()
