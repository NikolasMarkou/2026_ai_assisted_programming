# Starter kit: Patterns in AI-Assisted Programming

Everything here runs offline with Python 3.10 or newer and the standard library only.
No package install, no network and no API key are needed. Run every command from this folder.

## Check your machine first

```text
python3 check_env.py
```

It prints your Python version, whether git is installed, and which of `claude`, `codex`,
`cursor` and `opencode` are on your PATH. It exits with 1 only when Python is older than
3.10 or git is missing. A missing agent tool does not stop you: the offline scripted agent
needs none. Windows: use WSL2 or Git Bash, because the demos and the agent call a POSIX shell.

## What is in each folder

| Folder | What it holds | How to run it |
|---|---|---|
| `demos/` | 13 short scripts, one idea each, deterministic | `python3 demos/d3_tamper.py` |
| `agent/` | The minimal coding agent and its offline scripted model | `python3 agent/minimal_agent.py DIRECTORY` |
| `exercises/e1_sampler/` | A bigram next-word sampler with a temperature knob | `python3 exercises/e1_sampler/bigram.py --compare` |
| `exercises/e2/` | `slugify` stub and 11 tests | `cd exercises/e2 && python3 -m unittest -q` |
| `exercises/e3/` | A date parser with a bug and 5 failing tests | `cd exercises/e3 && python3 -m unittest -q` |
| `exercises/e4/` | 5 tasks for prompt-pattern practice | read `tasks.md` |
| `exercises/e5/` | A small module to extend and an AGENTS.md lint | `python3 exercises/e5/lint_agents_md.py AGENTS.md` |
| `exercises/e6/` | Spec for a notes service, a scaffold check, and a function stub | `python3 exercises/e6/check_scaffold.py DIRECTORY` |
| `exercises/e7/` | Test-first pricing task with a stdlib line-coverage tool | `cd exercises/e7 && python3 cov.py pricing.py` |
| `exercises/e8/` | Lab: a function of about 30 lines with 2 bugs and passing visible tests | `cd exercises/e8 && python3 -m unittest -q` |
| `exercises/e9/` | A stack trace, a buggy module and a four-question diagnostic | read `README.md` |
| `exercises/e11/` | An order module of about 100 lines with 6 planted smells, characterization tests and 2 checks | read `README.md` |
| `exercises/e12/` | A small app, a 3-file task with 2 checkpoints, guardrail examples per tool, `check_done.py` and `pev.py` | read `task.md` |
| `exercises/e13-untrusted/` | A repository with 3 planted traps that only write marker files, and a scripted agent that obeys them | read `exercises/e13-task.md` |
| `exercises/e14/` | 6 scenarios to classify and a table of your tool's data settings | read `scenarios.md` |
| `exercises/capstone/` | A bookmarks app with tests, a 4-feature backlog and a pull request template | read `backlog.md` |
| `evals/` | Mini eval harness, scripted flaky agent and 10 tasks | read `evals/README.md` |
| `AGENTS.md` | The instruction file of this kit, written for the tools | read it |

Each demo prints its result and ends with checks that stop the script if a number changed.
Demos 3, 4 and 10 use git: they create their repository in a temporary directory and
remove it. They never touch your own repository.

## The agent

`agent/minimal_agent.py` is one loop and one tool (bash). It runs shell commands in the
directory you give it, so work on a copy of the exercise:

```text
cp -r exercises/e3 e3_work
python3 agent/minimal_agent.py e3_work
```

An offline model answers, also when `ANTHROPIC_API_KEY` is set in your environment.
It follows fixed rules for exercise e3 and prints every step as ACT and OBSERVE lines.
With the flag `--live` and a key set, the same loop calls the Messages API over HTTPS using only `urllib`. That costs money and gives a real model a shell with no sandbox, so skip `--live` in the exercises. The shell tool does not inherit a variable whose name contains KEY, TOKEN, SECRET or PASSWORD. That does not keep the key from a live model: the agent process still holds it, and on Linux a shell command can read it from `/proc/$PPID/environ`. If you use `--live`, run it in a container.
A real harness checks permissions before each command and runs it inside a sandbox. This one does neither.

`agent/injected_agent.py` is a second scripted agent for exercise e13. It obeys instructions
that it finds in files, so that you can test a defence against it. It writes only marker
files in the folder you give it; see `exercises/e13-task.md`.

## Exercises and tests

Every exercise folder runs its tests with `python3 -m unittest -q`, started inside that folder.
Optional: `pytest` and `coverage` also work on these folders; nothing in the kit needs them.

## Python versions

The kit is verified on Python 3.12. The 13 demos and the tests of every exercise were also
run on Python 3.10, and every file parses as Python 3.10 syntax. Python 3.9 and older is
not supported, and `check_env.py` fails on it.
