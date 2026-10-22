"""Demo 13: you set the model, the run passed, and the code never read the setting.

Run: MODEL=local-small python3 demos/d13_ignored_setting.py
The last line then fails, which is the point. Without MODEL it passes.
Standard library only.
"""
import os

MODEL = "big-rented-model"  # the module constant that decides which model answers


def answer(question):
    return f"[{MODEL}] 4"


print("environment says MODEL =", os.environ.get("MODEL"))
print("answer         :", answer("2+2"))
# The usual check: it ran and printed 4, so the local model works.
# The check that can fail: compare the setting you asked for with the one in use.
wanted = os.environ.get("MODEL")
message = f"you asked for {wanted!r}, the run used {MODEL!r}"
assert wanted is None or wanted == MODEL, message

# Hidden check (not shown)
assert answer("2+2") == "[big-rented-model] 4"
