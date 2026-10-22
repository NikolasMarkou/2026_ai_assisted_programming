"""Demo 10: one ';' in a command the agent wrote changes real repository state.

Runs in a throwaway repository in a temporary directory. Needs git and a POSIX
shell. The clone target does not exist, so the clone fails without any network.
"""
import re
import subprocess
import tempfile
from pathlib import Path

GIT = "git -c user.name=x -c user.email=x@x"
workdir = tempfile.TemporaryDirectory()
repo = Path(workdir.name)


def sh(command):
    r = subprocess.run(command, shell=True, cwd=repo, capture_output=True, text=True)
    return r.stdout.strip()


for name in ("a.py", "b.py", "c.py"):
    (repo / name).write_text("x = 1\n")
sh(f"git init -q -b main && git add -A && {GIT} commit -qm one")
sh(f"{GIT} commit -q --allow-empty -m two")


def state():
    tracked = int(sh("git ls-files | wc -l"))
    on_disk = int(sh("ls *.py | wc -l"))
    status = sh("git status | head -2").splitlines()
    header = re.sub(r" at [0-9a-f]+", " at <hash>", status[0])
    return tracked, on_disk, header, status[1:]


def show(label):
    tracked, on_disk, header, extra = state()
    print(f"{label:14}: tracked={tracked} on-disk={on_disk} | {header}")
    return tracked, on_disk, header, extra


before = show("before")
# The agent wanted: clone a fixture repository, then work inside it. The clone fails.
sh("git clone -q /nonexistent/fixture.git fixture ; git sparse-checkout set a.py ;"
   " git checkout -q HEAD~1")
after_semicolon = show("after the ';'")
print("  ", *after_semicolon[3])
sh("git sparse-checkout disable && git checkout -q main")
sh("git clone -q /nonexistent/fixture.git fixture && cd fixture"
   " && git sparse-checkout set a.py")
after_and = show("with '&&'")

# Hidden check (not shown)
assert before[:3] == (3, 3, "On branch main")
assert after_semicolon[:3] == (3, 1, "HEAD detached at <hash>")
assert after_semicolon[3] == ["You are in a sparse checkout with 34% of tracked "
                              "files present."]
assert after_and[:3] == before[:3]
workdir.cleanup()
