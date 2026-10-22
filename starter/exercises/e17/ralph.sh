#!/bin/sh
# The Ralph loop in a POSIX shell: the same passes as ralph.py, started from the shell.
# Usage: sh exercises/e17/ralph.sh [MAX_PASSES]      (default 5; 0 is refused)
# Windows: this needs WSL or Git Bash. ralph.py does the same without a shell.
# Geoffrey Huntley's loop, as he wrote it, has no counter and no end:
#   while :; do cat PROMPT.md | claude-code ; done
# Here every pass is a new process (ralph.py --once) that reads PROMPT.md again, and
# the loop ends when fix_plan.md has no unchecked item or after MAX_PASSES passes.
MAX=${1:-5}
case $MAX in
  ''|*[!0-9]*|0*) echo "MAX_PASSES must be 1 or more: never unlimited" >&2
                 exit 2 ;;
esac
HERE=$(cd "$(dirname "$0")" && pwd)
WORK=$(mktemp -d "${TMPDIR:-/tmp}/ralph_sh_XXXXXX") || exit 2
trap 'rm -rf "$WORK"' EXIT
PLAN=$WORK/work/fix_plan.md
echo "SCRIPTED DEMONSTRATION by the course authors, not a measurement"
echo "ralph.sh: scripted model, up to $MAX passes, a new process each pass"
i=0
while [ "$i" -lt "$MAX" ]; do
  i=$((i + 1))
  python3 "$HERE/ralph.py" --once --dir "$WORK/work" || exit 1
  if ! grep -q '^- \[ \]' "$PLAN"; then
    echo
    echo "DONE: no open item after $i passes. The loop stopped itself."
    exit 0
  fi
done
echo
echo "STOP: MAX_PASSES $MAX reached with an item still open. No further pass will run."
grep '^- \[' "$PLAN"
exit 1
