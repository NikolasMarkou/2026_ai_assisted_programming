"""Build a linear walkthrough of a small Python file from real command output.

Usage: python3 exercises/e21/walkthrough.py [FILE]
Default FILE: agent_pr/cart.py next to this script. The script reads FILE with the
Python versions of three shell commands (`wc -l`, `grep -n -E`, `sed -n 'A,Bp'`),
prints each command, and prints what the command returned. Every line of code in the
walkthrough came out of one of those reads. The script holds no snippet of the file
typed by hand, and it takes every line number from an earlier read. Change a line of
FILE and the walkthrough changes with it.
This is our own small illustration of a linear walkthrough. It is not Simon Willison's
showboat tool. His walkthrough prompt tells the agent to use "sed or grep or cat" so
that it does not copy code by hand, which is the idea followed here.
It explains structure: size, the top of the file, each definition, the tests and the
entry point. It does not tell you whether the code is right. Exit code 0, or 2 when FILE
cannot be read. The commands are shown with the file name only, so the output is the
same on every machine.
Interface for other code: Reader(path) holds the file; Reader.wc(), Reader.grep(pattern)
and Reader.sed(first, last) each return the output lines and record the command in
Reader.commands; walk(reader) returns the lines of the walkthrough.
Standard library only.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT = HERE / "agent_pr" / "cart.py"
OUTLINE = r"^(def|class|if) "
TESTS = r"^ +def test_"


class Reader:
    """A file read through wc, grep and sed. Every call is recorded in commands."""

    def __init__(self, path):
        self.name = Path(path).name
        self.lines = Path(path).read_text(encoding="utf-8").splitlines()
        self.commands = []

    def wc(self):
        """The output of `wc -l NAME`."""
        self.commands.append(f"wc -l {self.name}")
        return [f"{len(self.lines)} {self.name}"]

    def grep(self, pattern):
        """The output of `grep -n -E 'PATTERN' NAME`: [(line number, text)]."""
        self.commands.append(f"grep -n -E '{pattern}' {self.name}")
        return [(number, text) for number, text in enumerate(self.lines, 1)
                if re.search(pattern, text)]

    def sed(self, first, last):
        """The output of `sed -n 'FIRST,LASTp' NAME`: the lines first to last."""
        self.commands.append(f"sed -n '{first},{last}p' {self.name}")
        return self.lines[first - 1:last]

    def last_filled(self, first, last):
        """Last line number in first..last that is not blank, read from the file."""
        while last > first and not self.lines[last - 1].strip():
            last -= 1
        return last


def block(reader, title, command_output):
    """A heading, the command just run, and its output (a list of lines)."""
    lines = ["", title, f"$ {reader.commands[-1]}"]
    return lines + [f"    {text}".rstrip() for text in command_output]


def numbered(rows):
    return [f"{number}:{text}" for number, text in rows]


def walk(reader):
    """The lines of the walkthrough. Each code line comes from a read of the file.

    Each block is built right after the read it shows, so the command line printed
    above an output is the command that produced it.
    """
    out = [f"Walkthrough of {reader.name}",
           "Each block is the output of the command above it. No code is typed in "
           "by hand."]
    out += block(reader, "1. Size", reader.wc())
    outline = reader.grep(OUTLINE)
    out += block(reader, "2. The top-level lines (what it defines, and its entry "
                 "point)", numbered(outline))
    definitions = [(n, text) for n, text in outline if not text.startswith("if ")]
    guards = [n for n, text in outline if text.startswith("if ")]
    if definitions and definitions[0][0] > 1:
        end = reader.last_filled(1, definitions[0][0] - 1)
        out += block(reader, "3. The top of the file, before the first definition",
                     reader.sed(1, end))
    stop = guards[0] if guards else len(reader.lines) + 1
    edges = [number for number, _ in definitions] + [stop]
    for index, (number, text) in enumerate(definitions):
        end = reader.last_filled(number, edges[index + 1] - 1)
        name = re.match(r"(?:def|class) (\w+)", text)
        out += block(reader, f"4.{index + 1} {name[1] if name else text}",
                     reader.sed(number, end))
    out += block(reader, "5. The tests", numbered(reader.grep(TESTS)))
    if guards:
        out += block(reader, "6. The entry point",
                     reader.sed(guards[0], len(reader.lines)))
    return out + ["", f"commands run: {len(reader.commands)}"]


def main(argv):
    if len(argv) > 1:
        print("usage: walkthrough.py [FILE]")
        return 2
    path = Path(argv[0]) if argv else DEFAULT
    try:
        reader = Reader(path)
    except OSError:
        print(f"cannot read: {path.name}")
        return 2
    print("\n".join(walk(reader)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
