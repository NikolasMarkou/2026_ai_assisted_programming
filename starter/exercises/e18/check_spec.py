"""Check a loop spec for exercise E18: are all five fields there, and are they usable?

Usage: python3 exercises/e18/check_spec.py SPEC.md [SPEC.md or FOLDER ...]
A spec is a markdown file with five sections: trigger, goal, verification, stopping
rule and memory (see spec_template.md). For each file the script prints one line per
field: ok, or FAIL with the reason. A folder means every .md file in it. Exit 0 when
every spec passes, 1 when any field of any spec fails, 2 when a path cannot be read.
What a field must hold:
  trigger        names an event (a push, a failing test, a schedule) or a command in
                 backticks. "When needed" is not one.
  goal           states an end state that someone can check: a number, a command in
                 backticks, "no unchecked item", "all tests pass".
  verification   names a command in backticks that can fail, and says it exits with a
                 non-zero status when the check is not met. "Looks good" is not one.
  stopping rule  has a success condition ("stop when ...") and a number of passes.
  memory         names a file path, such as progress.md.
This is a check of shape. It does not show whether the goal is the right goal or the
command a good test. The five-part list is one author's definition (arXiv 2607.00038),
not a standard. Our checker is a teaching tool made for this course.
Interface for other code: parse(text) returns {field: one-line body} for the sections
found; check(text) returns {field: [reasons]} with an empty list for a field that
passes; cap_of(body) returns the number of passes in a stopping rule or None;
memory_file_of(body) returns the first file path in a memory field or None.
Standard library only.
"""
import sys

sys.dont_write_bytecode = True
import re  # noqa: E402
import textwrap  # noqa: E402
from pathlib import Path  # noqa: E402

FIELDS = ("trigger", "goal", "verification", "stopping rule", "memory")
UNIT = r"(?:passes|pass|iterations?|attempts?|tries|turns|rounds|runs|loops)"
CAP_FLAG = re.compile(r"--max-iterations[ =]+(\d+)")
CAP_WORDS = re.compile(r"\b(\d+)\s+" + UNIT + r"\b", re.I)
VAGUE_TRIGGER = re.compile(
    r"\b(when needed|as needed|if needed|when necessary|when required|whenever|"
    r"when appropriate|when i feel|sometimes|from time to time|at some point)\b", re.I)
EVENT = re.compile(
    r"\bon (?:a |an |every |each |any )?(?:push|commit|merge|pull request|tag|release|"
    r"save|failing|failed|failure|schedule)\b|"
    r"\b(?:every|each) (?:\d+ )?(?:minutes?|hours?|days?|nights?|weeks?|mornings?|"
    r"commit|push|merge)\b|\b(?:daily|nightly|hourly|weekly|cron)\b|"
    r"\bafter (?:every|each) \w+|"
    r"\bwhen (?:a|an|the|any|each) [\w ]{1,40} (?:fails?|is opened|is pushed|"
    r"is merged|changes|is created|is saved|arrives)\b", re.I)
VAGUE_GOAL = re.compile(
    r"\b(better|nicer|improve[sd]?|good|cleaner|clean up|polish|optimi[sz]e|best)\b",
    re.I)
END_STATE = re.compile(
    r"`[^`]+`|\d|"
    r"\b(?:no|zero|none)\b[\w ]{0,30}\b(?:open|unchecked|failing|failed|errors?|left|"
    r"remaining|missing)\b|"
    r"\b(?:every|all)\b[\w ]{0,40}\b(?:ticked|checked|pass|passes|passing|done|closed|"
    r"fixed|green)\b|"
    r"\b(?:passes|pass|passed|exits? 0|exit status 0|is empty|equals?|matches)\b", re.I)
SPAN = re.compile(r"`([^`]+)`")
RUNNERS = {"make", "pytest", "tox", "nox", "ctest", "jest", "mocha", "vitest"}
CANNOT_FAIL = {"echo", "true", "printf", ":"}
FAILS = re.compile(
    r"non-?zero|exit(?:s|ed)? (?:status |code )?(?:of )?[1-9]|"
    r"\b(?:fails|failing|failure|fail)\b|returns? [1-9]", re.I)
SUCCESS = re.compile(
    r"\b(?:until|when|once|as soon as|if)\b.{0,80}?\b(?:pass|passed|passing|passes|"
    r"green|done|ticked|checked|empty|complete|completes|completed|finished|"
    r"succeeds?|met|true|exits? 0|left|remaining|open|fixed|solved|resolved|closed|"
    r"works|accepted)\b", re.I)
FILE = re.compile(
    r"(?<![\w./-])((?:[\w.-]+/)*[\w.-]+\.(?:md|txt|json|jsonl|tsv|csv|log|yaml|yml|"
    r"toml|ini|py))\b")


def parse(text):
    """The sections of a spec: {field: body on one line}. Comments are removed."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    found, current = {}, None
    for line in text.splitlines():
        heading = re.match(r"##\s+(.+?)\s*$", line)
        if heading:
            name = re.sub(r"[_-]+", " ", heading[1].lower()).strip()
            current = name if name in FIELDS else None
            if current:
                found[current] = []
        elif current and line.strip():
            found[current].append(line.strip())
    return {name: " ".join(" ".join(lines).split()) for name, lines in found.items()}


def cap_of(body):
    """The number of passes in a stopping rule, or None when there is no number."""
    match = CAP_FLAG.search(body) or CAP_WORDS.search(body)
    return int(match[1]) if match else None


def memory_file_of(body):
    """The first file path in a memory field, or None."""
    match = FILE.search(body)
    return match[1] if match else None


def command_spans(body):
    """Backtick spans that are commands: a program with arguments, or a known runner."""
    spans = [s.strip() for s in SPAN.findall(body)]
    return [s for s in spans if s and (" " in s or s.split()[0] in RUNNERS)]


def trigger_problems(body):
    if command_spans(body) or EVENT.search(body):
        return []
    vague = VAGUE_TRIGGER.search(body)
    said = f' "{vague[1]}" is not one.' if vague else ""
    return ["names no event and no command." + said + " Say what starts the run: a "
            "push, a failing test, a time of day, or a command in backticks."]


def goal_problems(body):
    if END_STATE.search(body):
        return []
    vague = VAGUE_GOAL.search(body)
    said = f' "{vague[1]}" cannot be checked.' if vague else ""
    return ["states no end state that can be checked." + said + " Write what is true "
            "when the loop has succeeded: a number, a command, an empty list."]


def verification_problems(body):
    commands = command_spans(body)
    if not commands:
        return ["names no command in backticks. A judgement such as \"looks good\" "
                "is not a check. Name a command that can fail."]
    if commands and all(c.split()[0] in CANNOT_FAIL for c in commands):
        return [f"the command `{commands[0]}` cannot fail, so it checks nothing."]
    if not FAILS.search(body):
        return ["does not say that the command exits with a non-zero status when the "
                "check is not met."]
    return []


def stopping_problems(body):
    problems = []
    cap = cap_of(body)
    rest = CAP_WORDS.sub("", CAP_FLAG.sub("", body))
    if not SUCCESS.search(rest):
        problems.append("has no success condition. Say when the loop stops because "
                        "the work is done, for example \"stop when no item is open\".")
    if cap is None:
        problems.append("has no number of passes (a cap). Write one, for example "
                        "\"after 5 passes\".")
    elif cap == 0:
        problems.append("the cap is 0. A loop needs a cap of 1 pass or more.")
    return problems


def memory_problems(body):
    path = memory_file_of(body)
    if not path:
        return ["names no file. Write the path of the file that keeps the state "
                "between passes, for example progress.md."]
    return []


RULES = {"trigger": trigger_problems, "goal": goal_problems,
         "verification": verification_problems, "stopping rule": stopping_problems,
         "memory": memory_problems}


def check(text):
    """Grade a spec. Returns {field: [reasons]}; an empty list means the field is ok."""
    body = parse(text)
    result = {}
    for field in FIELDS:
        if field not in body:
            result[field] = [f"missing. Add a section that starts with ## {field}."]
        elif not body[field] or "TODO" in body[field]:
            result[field] = ["not filled in."]
        else:
            result[field] = RULES[field](body[field])
    return result


def report(name, result):
    """Print the result of one spec. Returns True when every field is ok."""
    good = not any(result.values())
    print(f"{name}: {'PASS' if good else 'FAIL'}")
    for field in FIELDS:
        reasons = " ".join(result[field])
        print(textwrap.fill(f"  {field:<14}{'FAIL ' + reasons if reasons else 'ok'}",
                            width=96, subsequent_indent=" " * 16))
    return good


def paths_of(arguments):
    """The spec files named by the arguments; a folder gives its .md files in order."""
    paths = []
    for argument in arguments:
        path = Path(argument)
        paths += sorted(path.glob("*.md")) if path.is_dir() else [path]
    return paths


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.split("\n")[0])
        print("Usage: python3 exercises/e18/check_spec.py SPEC.md [SPEC.md|FOLDER ...]")
        return 2
    paths = paths_of(argv)
    if not paths:
        print("check_spec: no .md file found", file=sys.stderr)
        return 2
    passed = 0
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            print(f"check_spec: cannot read {path}: {error.strerror}", file=sys.stderr)
            return 2
        passed += report(path.name, check(text))
    if len(paths) > 1:
        print(f"{len(paths)} specs checked: {passed} pass, {len(paths) - passed} fail")
    return 0 if passed == len(paths) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
