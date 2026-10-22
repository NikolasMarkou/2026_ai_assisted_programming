"""The scripted worker for exercise E19: finish one slice and write one handoff line.

A worker is given its own slice and nothing else: no other slice, no other worker.
It reads the files its slice owns, replaces the stub in each with a fixed body, and
returns the edits it wants to make plus one handoff line. It does not write anything
itself: team.py applies each edit only if the path is in the slice, so the limit is
kept by the driver and not by the worker. With rogue=True the worker also asks to
change shop/interface.py (our script of a worker that is sure it knows better), to
show what the driver does with a write outside the slice.
Interface for other code: work(name, slice_body, root, rogue=False) returns
(edits, handoff): edits is a list of (relative path, new text) and handoff is one
line "name | status | files | note: ..." with status "done" or "nothing to do" (no
stub left in an owned file). BODIES maps an owned path to (code, note). Standard
library only.
"""
import sys

sys.dont_write_bytecode = True
import re  # noqa: E402
from pathlib import Path  # noqa: E402

STUB = re.compile(r"^    raise NotImplementedError\(.*\)\n", re.M)
BODIES = {
    "shop/parse.py": ("""\
    lines = []
    for raw in text.splitlines():
        if not raw.strip():
            continue
        left, _, price = raw.rpartition("@")
        qty, _, name = left.partition(" x ")
        euros, _, fraction = price.strip().partition(".")
        cents = int(euros) * 100 + int((fraction + "00")[:2])
        lines.append(Line(name.strip(), int(qty), cents))
    return lines
""", "the price text is cut at 2 decimals, not rounded"),
    "shop/total.py": ("""\
    subtotal = sum(line.qty * line.cents for line in lines)
    if subtotal >= 10000:
        subtotal -= subtotal // 10
    return subtotal
""", "the discount is integer division, so 12345 gives 11111"),
    "shop/render.py": ("""\
    rows = [f"{line.name} x{line.qty}: {money(line.qty * line.cents)}"
            for line in lines]
    rows.append(f"TOTAL: {money(total_cents)}")
    return "\\n".join(rows)
""", "every amount goes through money() from the interface"),
}
ROGUE_PATH = "shop/interface.py"
ROGUE_OLD, ROGUE_NEW = "{cents % 100:02d}", "{cents % 100}"
ROGUE_NOTE = "also wanted money() to drop the zero padding of the cents"


def work(name, slice_body, root, rogue=False):
    """Edits and the handoff line of worker name for its slice. Writes nothing."""
    edits, notes = [], []
    for path in slice_body["owns"]:
        body, note = BODIES.get(path, (None, f"no script for {path}"))
        text = Path(root, path).read_text(encoding="utf-8")
        if body is not None and STUB.search(text):
            edits.append((path, STUB.sub(lambda _: body, text, count=1)))
            notes.append(note)
        elif body is not None:
            notes.append("the stub is already replaced")
        else:
            notes.append(note)
    if rogue:
        text = Path(root, ROGUE_PATH).read_text(encoding="utf-8")
        edits.append((ROGUE_PATH, text.replace(ROGUE_OLD, ROGUE_NEW)))
        notes.append(ROGUE_NOTE)
    status = "done" if edits else "nothing to do"
    files = ", ".join(slice_body["owns"])
    return edits, f"{name} | {status} | {files} | note: {'; '.join(notes)}"
