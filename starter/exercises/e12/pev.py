"""Plan, execute, verify with a retry cap, then stop and show.

    python3 pev.py --agent "COMMAND" --verify "COMMAND" [--plan plan.md] [--yes]

PLAN: with --plan the file is printed and a person must type y (--yes skips the question
for scripts and tests). EXECUTE: the agent command runs once. VERIFY: the verify command
runs; exit 0 is green. A red verify spends one of the FIX_CAP fix attempts and the agent
runs again with PEV_ATTEMPT (0 is the first run) and PEV_FAILURE (the last output of the
verify command) in its environment. After FIX_CAP failed fixes the driver stops, prints
what was tried and what failed, and never runs a third fix.
Exit 0 green, 1 stopped and shown, 2 plan not approved or a usage error.
Standard library only.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

FIX_CAP = 2  # fix attempts after the first run; the stop-and-show rule of the day


def sh(command, cwd, **env):
    """Run a shell command. Returns (exit code, output lines) with stderr included."""
    done = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True,
                          env={**os.environ, **env})
    return done.returncode, (done.stdout + done.stderr).strip().splitlines()


def run_step(agent, verify, cwd, cap=FIX_CAP):
    """Run agent, then verify; each red verify spends one of cap fix attempts.

    Returns (status, history). status is "green" or "stopped". history has one
    (attempt, agent's last line, verify exit code, verify output lines) per agent run.
    """
    history, failure = [], ""
    for attempt in range(cap + 1):
        _, said = sh(agent, cwd, PEV_ATTEMPT=str(attempt), PEV_FAILURE=failure)
        code, output = sh(verify, cwd)
        history.append((attempt, said[-1] if said else "(no output)", code, output))
        if code == 0:
            return "green", history
        failure = "\n".join(output[-15:])
    return "stopped", history


def stop_and_show(history):
    """Print what was tried and what failed. The person decides what happens next."""
    print(f"STOP: verify is still red after {len(history) - 1} fix attempts. "
          "No further attempt will run.")
    print("what was tried:")
    for attempt, said, code, output in history:
        last = output[-1] if output else "(no output)"
        print("  first run" if attempt == 0 else f"  fix attempt {attempt}")
        print(f"    agent said: {said}")
        print(f"    verify exit {code}: {last}")
    print("what failed (output of the last verify):")
    for line in history[-1][3][-15:]:
        print(f"  {line}")
    print("next: you decide. Revert the changes, fix it by hand, or change the task.")


def approved(plan, yes):
    """Print the plan and ask. No answer (closed input) counts as no."""
    print(Path(plan).read_text(encoding="utf-8"))
    try:
        return yes or input("Approve this plan? [y/N] ").strip().lower() == "y"
    except EOFError:
        return False


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--agent", required=True)
    parser.add_argument("--verify", required=True)
    parser.add_argument("--cwd", default=".")
    parser.add_argument("--plan")
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args(argv)
    if args.plan and not approved(args.plan, args.yes):
        print("plan not approved: nothing was run")
        return 2
    status, history = run_step(args.agent, args.verify, args.cwd)
    if status == "stopped":
        stop_and_show(history)
        return 1
    print(f"GREEN after {len(history) - 1} fix attempts. "
          "Show the diff to the person and wait for approval before you merge.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
