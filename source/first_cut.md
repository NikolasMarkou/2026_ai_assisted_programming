<!-- SOURCE: the user's first cut, pasted verbatim on 2026-10-21 (invocation of /iterative-planner). Only change: the pasted escaped bang characters (backslash-bang) were restored to plain "!" in two code listings. Do not edit; this is the source of record. -->

# Patterns in AI-Assisted Programming

Practitioner guide, October 2026. Covers Cursor, Codex, Claude Code and OpenCode.

---

## 0. Schedule

- **Programme:** Patterns in AI-Assisted Programming (ΑνΑΔ programme no. 749209)
- **Date:** 22/10/2026
- **Duration:** 6 teaching hours

| Time | Block | Guide sections |
|---|---|---|
| 09:00-11:00 | **Session 1: Foundations, Tools and Prompt Engineering** | 1, 2, 3, 4, 5 |
| 11:00-11:15 | Break | |
| 11:15-13:15 | **Session 2: Code Generation Patterns and AI-Driven Testing** | 6, 8 |
| 13:15-14:00 | Lunch | |
| 14:00-16:00 | **Session 3: Agentic Workflows, Refactoring and Responsible Use** | 7, 9, 10 |

### Format: every block is hands-on

Every block follows the same rhythm:

1. **Show (max 10 min):** the instructor explains one concept and demonstrates it live.
2. **Do (15 to 30 min):** every participant performs an exercise on their own machine, in their own tool.
3. **Share (2 to 3 min):** two or three participants show a result, a surprise, or a failure.

Participants work in **pairs using different tools** where possible (for example Cursor + Claude Code, Codex + OpenCode), so every exercise also produces a tool comparison. Exercise details are in section 11; machine setup must be completed **before** the training (section 12).

### Session 1 (09:00-11:00)

| Time | Show (instructor) | Do (participants) | Exercise |
|---|---|---|---|
| 09:00-09:15 | Course goals, the hands-on format | Clone the starter repo, open your tool, ask the agent to explain the repo structure | E0 |
| 09:15-09:35 | Tokens, next-token prediction, training phases (1.1) | Count tokens of code vs prose; run one prompt 3 times at low and high temperature; compare | E1 |
| 09:35-09:55 | The ladder: autocomplete, chat, agent, cloud, swarms (1.2) | Implement the same function three ways: autocomplete, chat, agent; record time and correctness | E2 |
| 09:55-10:15 | The ReAct loop and the harness (3) | Run the minimal agent, or inspect your tool's transcript and context usage; label each tool call | E3 |
| 10:15-10:35 | Prompt patterns (5) | Write five prompts for real tasks using at least three patterns; compare outputs with your pair | E4 |
| 10:35-11:00 | AGENTS.md, skills, plan mode (4, 5) | Write an AGENTS.md; re-run a prompt with and without it; run one task through plan mode first | E5 |

### Session 2 (11:15-13:15)

| Time | Show (instructor) | Do (participants) | Exercise |
|---|---|---|---|
| 11:15-11:40 | Scaffold and function completion (6) | Scaffold a small service from a one-paragraph spec; then complete a function from signature, docstring and examples | E6 |
| 11:40-12:05 | TDD loop, coverage-driven prompting (6) | Tests first, confirm failure, commit, implement; push branch coverage to a target | E7 |
| 12:05-12:35 | Lab briefing (2 min) | **Lab:** 30-line function with two known bugs; generate tests, find and fix both, confirm green | E8 |
| 12:35-12:55 | Bug diagnosis, regression guarding (6) | Diagnose a provided stack trace; make a change and have AI review the diff and list missing tests | E9 |
| 12:55-13:15 | Evals as engineering (8) | Run the mini eval: 3 tasks, 2 trials, with and without one AGENTS.md rule; post scores to the shared table | E10 |

### Session 3 (14:00-16:00)

| Time | Show (instructor) | Do (participants) | Exercise |
|---|---|---|---|
| 14:00-14:20 | Code smells, safe refactoring, auto-docs (6, 7) | Rank smells in a legacy module; fix the top one with tests green before and after; generate its README section | E11 |
| 14:20-14:45 | Plan, Execute, Verify; checkpoints; permissions (7, 3.11, 3.12) | Add guardrails (deny rules, a test hook or done criteria); run a multi-step task with explicit checkpoints; try two attempts in parallel | E12 |
| 14:45-15:05 | Prompt injection and the agent attack surface (10) | Security drill: run an agent on a booby-trapped repo in a sandbox; find the injection; harden the setup | E13 |
| 15:05-15:15 | Evidence, IP, skill atrophy, when not to use AI (9, 10) | Classify six scenarios as "use AI / use with heavy review / avoid"; check your tool's data and privacy settings | E14 |
| 15:15-15:50 | Capstone briefing (5 min) | **Capstone:** one feature end to end: spec, plan, checkpoint, TDD, AI review, PR | E15 |
| 15:50-16:00 | | **Final evaluation:** submit the capstone PR link and complete the short assessment | |

---

## 1. The Landscape: From Tokens to Agent Swarms

Each layer below is built from the one before it. If you understand the layer underneath, the behavior (and the failure modes) of the layer above stops being magic.

```text
tokens -> LLM -> trained model -> autocomplete -> chat -> agent -> cloud agent -> swarms
          (predict)  (shaped)       (+ position)    (+ roles) (+ tools  (+ remote    (+ many agents
                                                               + loop)   sandbox)     coordinating)
```

### 1.1 The primitives: how LLMs are made

#### Step 1: Tokens

- Models never see characters or words. A **tokenizer** splits text into sub-word pieces (typically byte-pair encoding) and maps each piece to an integer ID.
- In English prose a token averages roughly 3 to 4 characters. Code tokenizes less efficiently: indentation, punctuation, and long identifiers like `getUserAccountBalance` split into several tokens.
- Everything is measured in tokens: the **context window** (how much the model can see at once, today from hundreds of thousands up to about a million tokens), **cost** (priced per input and output token) and **latency** (output is generated one token at a time).
- Consequences for coding: models are weak at character-level tasks (counting characters, exact column alignment, long hex strings) because they operate on chunks, not letters. A large log file is not "one file" to the model; it is tens of thousands of tokens of budget.

#### Step 2: The LLM, a next-token predictor

- An LLM is a transformer network. Each token ID becomes a vector (an **embedding**). Stacked **attention** layers let every position draw information from every earlier position in the context.
- The output is a **probability distribution over the next token**. The model picks one (**sampling**), appends it, and repeats. This is **autoregressive generation**.
- **Temperature** and related settings control how adventurous sampling is. Low temperature gives repeatable, conservative output; higher gives more variety and more mistakes.
- The model has no memory between calls and no built-in ability to run code. Everything it "knows" during a request is either in its weights (from training) or in the context window (from you or its tools).
- Key insight for coding: the model produces the most plausible continuation, not a verified one. Plausible and correct usually coincide, which is why this works; when they diverge, you get confident, idiomatic, wrong code.

#### Step 3: Training phases, how a predictor becomes a coding assistant

| Phase | What happens | What it adds | Side effects you will meet |
|---|---|---|---|
| **Pretraining** | Next-token prediction over trillions of tokens of web text, books and public code | Language, world knowledge, programming languages, common libraries and idioms | Knowledge stops at a **cutoff date**; outdated or deprecated APIs feel "correct" to the model |
| **Mid-training** | Continued training on curated, code-heavy and long-document data; objectives like fill-in-the-middle | Long-context skill, editing inside existing code | Better at code it has seen patterns of; weaker on private or niche frameworks |
| **Supervised fine-tuning (SFT)** | Training on curated example conversations and demonstrations | Follows instructions, uses a chat format with roles | Learns a "helpful assistant" style, including over-eagerness |
| **Preference tuning** (RLHF, RLAIF, DPO) | Learning from comparisons of better vs worse answers, judged by humans or AI against principles | Helpfulness, harmlessness, tone, refusing unsafe actions | Can favor answers that *look* good to a grader |
| **Reinforcement learning on verifiable rewards** | The model attempts tasks in sandboxes with tools; rewards come from objective checks such as unit tests passing | Multi-step reasoning ("thinking"), tool use, persistence across long agentic tasks; this is what made 2025 to 2026 agents work | **Reward hacking**: learned shortcuts like editing tests, special-casing inputs, or declaring success early (see sections 3.13 and 8.9) |

Two practical takeaways:

- The model's knowledge is frozen at training time. Fresh information (your codebase, current docs, today's library versions) must come through the **context window**, which is why context engineering matters so much.
- Modern coding models are explicitly trained to use tools in loops against tests. They work best when you give them that environment: a runnable repo, a test command and a clear definition of done.

### 1.2 The ladder: from autocomplete to swarms

Each rung reuses the same trained model family but wraps it in more machinery and hands it more autonomy.

#### Rung 1: Autocomplete

- **Mechanism**: fill-in-the-middle (FIM). The editor sends the code before the cursor (prefix) and after it (suffix); a small, fast model predicts the middle. Latency must stay in the low hundreds of milliseconds, so these models are smaller than chat models.
- **Evolution**: next-edit prediction, where the model also predicts *where* you will edit next and proposes the change there (Cursor Tab works this way).
- **Context**: the current file plus nearby or recently opened files.
- **Human role**: accept or reject keystroke by keystroke. You remain the author.
- **Fails at**: anything requiring knowledge outside the visible context, or multi-file changes.

#### Rung 2: Chat

- **Mechanism**: an instruction-tuned model with a **chat template**: a system message, then alternating user and assistant turns. The full history is re-sent on every turn because the model is stateless.
- **Context**: whatever you paste in, plus files you attach or mention.
- **Human role**: you are the tool loop. You copy code in, run it, read errors, and paste results back.
- **Fails at**: staying grounded in your real codebase; every fact it has comes from what you chose to paste.

#### Rung 3: Agent

- **Mechanism**: a tool-calling model inside a **harness loop**. The model requests actions (read, search, edit, run tests), the harness executes them and feeds results back, until the task is done. This is the ReAct loop, covered in depth in section 3.
- **Context**: the agent gathers its own context by exploring the repo, plus instruction files (AGENTS.md / CLAUDE.md), skills and tools.
- **Human role**: set the goal, approve risky actions, review the plan and the diff.
- **Fails at**: long tasks without a clear stopping check, ambiguous goals, and untrusted inputs (prompt injection).

#### Rung 4: Cloud agent

- **Mechanism**: the same agent loop running in an isolated remote VM or container with a full development environment. It works asynchronously for minutes to hours and delivers a **pull request**.
- **Requirements**: a reproducible environment setup script, a test suite the agent can run, and a policy for secrets and network access.
- **Human role**: write a good ticket or spec up front, review the PR at the end. Supervision moves from watching steps to reviewing outcomes.
- **Fails at**: underspecified tickets and environments that cannot build or test the project. If CI is weak, review becomes the bottleneck.
- **Examples**: Cursor cloud agents, Codex Cloud, Claude Code cloud sessions, GitHub Copilot cloud agent.

#### Rung 5 (emerging): Swarms and multi-agent systems

- **Mechanism**: many agents coordinating on one goal. Common shapes:
  - **Orchestrator and workers**: a lead agent splits work, delegates to subagents, merges results.
  - **Specialist roles**: planner, implementer, tester and reviewer, often on different models.
  - **Parallel exploration**: several agents attempt the same task in separate worktrees; the best result wins.
  - **Always-on, event-driven agents**: agents subscribed to PRs, CI, issues or chat channels that wake up and act when something happens.
- **Where it shows up today**: nested and background subagents and agent teams in Claude Code, subagents on their own machines and event subscriptions in Cursor, multi-agent orchestration in Codex, background subagents in OpenCode.
- **Open problems**: coordination and shared state (merge conflicts, duplicated work), errors compounding across agents, costs multiplying with each agent, and a review bottleneck that grows with output volume.
- **Human role**: shifts toward specifying intent, designing the verification system (tests, evals, CI gates) and reviewing outcomes. This is why section 8 treats evals as a core engineering skill.

#### The ladder at a glance

| Rung | New primitive | Who closes the loop | Unit of human review | Main risk |
|---|---|---|---|---|
| Autocomplete | Fill-in-the-middle | You, per keystroke | A line | Subtle bugs accepted on autopilot |
| Chat | Roles and conversation history | You, by copy-paste | A snippet | Code detached from the real codebase |
| Agent | Tools and the harness loop | The agent, with your approvals | A diff | Wrong but plausible changes, prompt injection |
| Cloud agent | Remote sandbox, async execution | The agent, against CI | A pull request | Weak specs and weak tests |
| Swarm | Coordination between agents | Agents checking agents | A system outcome | Compounding errors, cost, review overload |

Think of this as an autonomy slider. Each rung up raises output volume and lowers how closely you watch each step, so **verification has to move into the system**: tests, hooks, CI, review agents and evals. The model's ability to write code is no longer the scarce resource; the ability to specify and verify it is.

---

## 2. The Four Tools

### 2.1 Comparison

| | Cursor | Codex | Claude Code | OpenCode |
|---|---|---|---|---|
| Form | AI-native IDE (VS Code fork), Agents Window, cloud agents, mobile, SDK | ChatGPT desktop app, CLI, IDE extension, Codex Cloud, mobile remote | CLI, VS Code and JetBrains extensions, desktop, web and cloud sessions | Background service shared by terminal TUI, web and desktop clients; SDK |
| Models | Composer 2.5 (Cursor's own) plus multi-vendor | OpenAI GPT-6 family (GPT-6.1 Sol, GPT-6 Luna) | Anthropic Claude (Opus 5.5, Sonnet 5.5, Haiku 5.5) | Any provider via your own key, including local models |
| Open source | No | CLI yes | No | Yes (MIT) |
| Instruction file | AGENTS.md, rules | AGENTS.md | CLAUDE.md | AGENTS.md |
| Parallelism | Many agents across worktrees, cloud and SSH; subagents on their own VMs | Subagents, managed git worktrees, cloud tasks | Background subagents, agent teams, worktrees | Background subagents with worktree isolation |
| Safety controls | Command allowlists, auto-review | OS sandbox, permission profiles, Auto-review agent | Permission modes (Manual, Auto), sandbox, hooks | Per-tool permissions, per-project auto-accept |
| Best demo angle | The full autocomplete to cloud-agent spectrum in one product | Long-running goals and sandboxed autonomy | The agentic loop, hooks, plan mode, code review | Model-agnostic: same harness, different models |

### 2.2 Cursor

- **Agents Window**: a dedicated surface for running many agents in parallel, locally, in git worktrees, in the cloud, or over SSH.
- **Cloud agents**: run in isolated VMs with a full dev environment, check out the repo, do the work, and open a PR. They can subscribe to events (PR activity, Slack threads, schedules) and keep driving their own PRs, including fixing CI and answering bot comments.
- **Self-hosted machines**: cloud agents can execute on machine pools inside your own network while Cursor handles orchestration.
- **Side chats** (`/side`, `/btw`): branch a secondary conversation off a running agent without interrupting it.
- **Bugbot**: AI review on pull requests.
- **Cursor SDK** (TypeScript and Python): programmatic agents, custom tools, nested subagents, auto-review for headless runs.
- **Steering**: type a follow-up while the agent works; it is applied at the next tool call instead of cutting the agent off.

### 2.3 Codex (OpenAI)

- **Surfaces**: part of the ChatGPT desktop app (macOS, Windows, Linux preview), plus the open-source CLI, IDE extension, Codex Cloud, and mobile remote control of a desktop host.
- **Goal mode** (`/goal`): Codex keeps driving toward a stated objective for hours or days.
- **Auto-review**: eligible approval prompts are routed through a reviewer agent first, which reports a status and risk level before you decide.
- **Permissions and sandboxing**: permission profiles plus OS-level sandboxing; actions that cross the sandbox boundary need approval.
- **Hooks, skills, plugins, MCP**: extensibility comparable to the other tools.
- **Code review**: review diffs and GitHub PRs inside the app; `@codex` on GitHub and GitLab issues or merge requests starts cloud tasks.
- **Browser and computer use**: Codex can drive an in-app browser to verify a UI fix, and can operate desktop apps.
- **Import**: brings instructions, skills, plugins and recent work over from Claude Code and Cursor (`/import` in the CLI).
- **Non-interactive**: `codex exec` for scripts and CI.

Model selection in the CLI:

```bash
codex --model gpt-6.1-sol      # complex, long-running work
codex --model gpt-6-luna       # focused, high-volume tasks
```

### 2.4 Claude Code (Anthropic)

- **Agentic loop**: explore, plan, edit, run, verify, in the terminal, IDE, desktop or cloud.
- **Plan mode**: the agent investigates and proposes a plan without editing. You approve it, then it executes.
- **Permission modes**: Manual (asks before acting) and Auto (a safety classifier decides per action). `/auto-mode-setup` tunes auto mode to your project.
- **Subagents**: run in the background by default, each with its own context, tools and model.
- **Hooks**: deterministic scripts on events such as PreToolUse, PostToolUse, SessionStart and Stop. Use them to run tests and linters automatically or to block dangerous commands.
- **Skills and plugins**: packaged instructions and tools, loaded on demand.
- **Worktrees**: `claude --worktree` isolates parallel work.
- **Code Review**: automatic GitHub PR review with Quick, Standard and Deep levels.
- **Headless**: `claude -p "..."` for scripts and CI; the Agent SDK for building your own agents.
- **Sandboxing**: OS-level isolation of shell commands.

### 2.5 OpenCode (open source)

- **Architecture**: one background service shared by terminal, web and desktop clients. Sessions survive closing a terminal.
- **Provider-agnostic**: bring your own API key, sign in with a supported subscription, or point it at local or OpenAI-compatible endpoints.
- **Code Mode**: the agent writes a short JavaScript script that calls and combines several tools in one execution. It is on by default for MCP servers and cuts context overhead.
- **Background subagents**: delegate, for example, a code review to a subagent running a different model while the main agent keeps working.
- **SDK**: `@opencode/sdk` embeds OpenCode in your own apps; `@opencode/client` talks to the server API.
- **Instructions**: reads `AGENTS.md` only.

Install or upgrade:

```bash
opencode upgrade --major        # from the latest 1.x to 2.x
```

Note: Anthropic consumer subscriptions cannot be used in third-party harnesses. To run Claude models in OpenCode, use an Anthropic API key.

---

## 3. How Coding Agents Work Internally

### 3.1 Model vs harness

An agent is a model plus a harness. The model only ever reads tokens and writes tokens. The harness does everything else:

| Harness component | Responsibility |
|---|---|
| System prompt | Behavior rules, environment facts (OS, cwd, date, git status), tool usage guidance |
| Tool registry | Names, descriptions and JSON Schemas of every tool the model may call |
| Loop controller | Sends requests, executes tool calls, feeds results back, decides when to stop |
| Context manager | Decides what stays in the window: instruction files, history, tool results, summaries |
| Permission layer | Allow / ask / deny rules, classifiers, approval prompts |
| Sandbox | OS-level isolation of whatever the agent executes |
| Extensibility | Hooks, skills, plugins, MCP clients, subagents |

The same model behaves differently in different harnesses. This is why benchmarks report "model + harness" and why switching tools changes results even with the same model.

### 3.2 The ReAct loop

ReAct (Reason + Act, Yao et al., 2022) interleaves reasoning with actions and observations:

```text
Thought:      the tests fail in parse_date; I need to see the function
Action:       read_file("src/dates.py")
Observation:  <file contents>
Thought:      the format string ignores timezone offsets
Action:       edit_file(...)
Observation:  edit applied
Action:       bash("pytest -q tests/test_dates.py")
Observation:  5 passed
Final answer: fixed timezone handling in parse_date; all tests pass
```

Modern agents implement this with native tool calling rather than parsing text. On the Claude API the cycle looks like this:

1. The harness sends the conversation plus a `tools` array.
2. If the model wants to act, the response ends with `stop_reason: "tool_use"` and contains one or more `tool_use` blocks, each with an `id`, a tool `name` and a structured `input`.
3. The harness executes each call and replies with a user message containing one `tool_result` block per call, matched by `tool_use_id`. Tool results come first in that message.
4. Repeat until the model answers without calling a tool (`stop_reason: "end_turn"`), or a limit is hit.

Other providers use the same shape under different names (function calls and function call outputs). Several independent calls in one response are "parallel tool use", which is how an agent reads five files in one step.

### 3.3 A minimal coding agent

The whole idea fits in about 40 lines. One tool (bash) is enough to read, search, edit and test.

```python
import subprocess
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

SYSTEM = (
    "You are a coding agent working in the current repository. "
    "Inspect before editing. After every change, run the tests. "
    "Only finish when the tests pass, then summarize what you changed."
)

TOOLS = [{
    "name": "bash",
    "description": (
        "Run a shell command in the repository root and return stdout and stderr. "
        "Use it to list, read, search and edit files and to run tests."
    ),
    "input_schema": {
        "type": "object",
        "properties": {"command": {"type": "string", "description": "Shell command"}},
        "required": ["command"],
    },
}]

def run_bash(command: str) -> str:
    # A real harness checks permissions and runs this inside a sandbox.
    r = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)
    out = r.stdout + r.stderr
    return out[-10_000:] or "(no output)"   # truncate to protect the context window

def agent(task: str, max_turns: int = 30) -> str:
    messages = [{"role": "user", "content": task}]
    for _ in range(max_turns):
        resp = client.messages.create(
            model="claude-sonnet-5-5", max_tokens=4096,
            system=SYSTEM, tools=TOOLS, messages=messages,
        )
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":                      # Act phase is over
            return "".join(b.text for b in resp.content if b.type == "text")
        results = [
            {"type": "tool_result", "tool_use_id": b.id, "content": run_bash(b.input["command"])}
            for b in resp.content if b.type == "tool_use"       # parallel calls supported
        ]
        messages.append({"role": "user", "content": results})   # Observation phase
    return "Stopped: turn limit reached"

print(agent("The tests in tests/test_dates.py fail. Find and fix the bug."))
```

Run it only in a throwaway container: it executes whatever the model asks for. Everything a production harness adds (permissions, sandboxing, compaction, subagents, hooks, specialized edit tools) is a refinement of this loop.

### 3.4 What the model actually sees

The model is stateless. Every turn, the harness re-sends the full request:

```text
[system prompt]          harness rules + environment info
[tool definitions]       names, descriptions, JSON Schemas (skills listed as one-liners)
[instruction files]      AGENTS.md / CLAUDE.md contents
[conversation]           user task
                         assistant: thinking + tool_use
                         user: tool_result
                         assistant: tool_use ...
                         ...
```

Consequences:

- **Prompt caching** makes this affordable. The stable prefix (system prompt, tools, instruction files) is cached and re-read cheaply. Changing early context, switching models, or toggling tools mid-session breaks the cache and costs more.
- **Every tool result costs tokens on every later turn** until it is removed or summarized. A careless `cat` of a 5,000-line log poisons the rest of the session.
- **Instructions and data share one channel.** A tool result containing "ignore previous instructions" is just more text to the model. This is the root cause of prompt injection.

### 3.5 Tools: design matters

Typical coding-agent toolset:

| Tool | Why it exists |
|---|---|
| Read (with line ranges) | Load only what is needed |
| Grep / Glob | Agentic search: find code by pattern instead of reading everything |
| Edit (`str_replace` or patch) | Change a unique snippet instead of rewriting whole files; cheaper and verifiable |
| Write | Create new files |
| Bash / shell | Run tests, builds, git; the universal escape hatch |
| Web fetch / search | Docs and current information |
| Todo / plan | Externalized task list that keeps long runs on track |
| Task / subagent | Delegate work to a fresh context |

Design principles:

- **Descriptions are prompts.** The model chooses tools from their names and descriptions. Vague descriptions produce wrong calls.
- **Errors are feedback.** Return actionable messages ("old_str matched 3 times; include more surrounding lines") rather than stack traces.
- **Truncate and paginate.** Large outputs should be cut, summarized or written to a file the agent can page through.
- **Fewer, sharper tools beat many overlapping ones.** Every tool definition costs context on every turn.
- **Agentic search vs embeddings.** Most coding agents now prefer iterative grep/glob/read over vector retrieval: it is always fresh, exact, and needs no index.

### 3.6 Context engineering and memory

Context is a finite budget, and quality degrades as it fills ("context rot"). Harnesses manage it with several techniques:

| Technique | What it does |
|---|---|
| Just-in-time loading | Keep file paths and identifiers; read contents only when needed |
| Tool-result clearing | Drop old, bulky tool outputs once they have served their purpose |
| Compaction | Summarize older turns into a short state description and continue in a fresh window |
| Memory files | Persist decisions and progress to disk (AGENTS.md, progress notes, todo lists) so they survive compaction and new sessions |
| Subagents | Give a subtask a clean window and return only a condensed result |

Subagents are context isolation, not just parallelism. A research subagent may read 40 files and return 20 lines. The main agent's window stays clean.

### 3.7 Skills: progressive disclosure

A skill is a folder with a `SKILL.md` file (YAML frontmatter plus instructions) and optional scripts, templates and references. Skills load in three levels:

```text
Level 1  name + description     always in context, a few dozen tokens per skill
Level 2  SKILL.md body           read only when the task matches the description
Level 3  bundled files/scripts   read or executed only when the instructions need them
```

This lets an agent have hundreds of skills installed while paying context only for the ones in use. Bundled scripts run as code, so their output (not their source) enters the context.

```markdown
---
name: release-notes
description: Write release notes from merged PRs in our house format. Use when asked for release notes or a changelog entry.
---
1. Run `scripts/merged_prs.sh <since-tag>` to list merged PRs.
2. Group by label: feature, fix, chore. Drop chore.
3. Follow templates/release.md exactly. One line per PR, imperative mood.
```

Skills vs other mechanisms:

| Mechanism | Provides | Loaded |
|---|---|---|
| AGENTS.md / CLAUDE.md | Always-relevant project facts and rules | Every session |
| Skill | Procedural know-how for a kind of task | On demand |
| MCP server | New capabilities (tools, data access) | Tool schemas at start or via tool search |
| Hook | Deterministic enforcement outside the model | On events |
| Subagent | A separate worker with its own context and tools | When delegated |

### 3.8 MCP under the hood

- **Architecture**: the host (Claude Code, Cursor, Codex, OpenCode) runs one MCP client per server. Messages are JSON-RPC 2.0.
- **Transports**: `stdio` (the host spawns the server as a local process) or Streamable HTTP (remote server).
- **Server primitives**: tools (actions), resources (readable data), prompts (templates).
- **Client primitives**: elicitation (the server asks the user for input) and sampling (the server asks the host's model to generate).
- **Tool search / deferred loading**: with many servers, tool schemas are not all sent up front. The agent searches for and loads the tools it needs, saving context.
- **Security implication**: a `stdio` server is an ordinary process with your user's privileges. A repo-defined MCP config that the agent auto-starts is code execution.

### 3.9 Code Mode and programmatic tool calling

Classic tool calling costs one model turn per call, and every intermediate result passes through the context window. In Code Mode the model writes a short script that calls several tools, filters and joins the results, and returns only the final output:

```javascript
// One execution instead of three model turns
const issues = await jira.search({ jql: "fixVersion = 2.4 AND status = Done" });
const prs = await github.listMergedPRs({ since: "v2.3.0" });
const missing = issues.filter(i => !prs.some(p => p.title.includes(i.key)));
return missing.map(i => `${i.key}: ${i.summary}`);
```

Benefits: fewer turns, much less context, and loops or filters run as real code instead of model reasoning. OpenCode 2.0 enables this by default for MCP servers; other platforms offer equivalent programmatic tool calling.

### 3.10 Planning, thinking and long runs

- **Plan mode** is usually a restricted tool set (read and search only) plus a prompt asking for a plan. It is a harness constraint, not a different model.
- **Extended / adaptive thinking**: the model reasons in a hidden or summarized block before acting. Higher effort settings buy better plans at higher latency and cost.
- **Todo lists** externalize the plan into context so the agent can tick items off and resist drift.
- **Goal modes and loops** keep re-prompting the agent until an objective check passes (tests green, coverage met), with progress written to files between iterations.

### 3.11 Hooks: deterministic control

Instructions in AGENTS.md are probabilistic: the model usually follows them. Hooks are deterministic: the harness always runs them.

| Event | Typical use |
|---|---|
| SessionStart | Inject branch status, ticket context, environment checks |
| UserPromptSubmit | Block prompts containing secrets; add context |
| PreToolUse | Block `rm -rf`, writes to `migrations/`, reads of `.env` |
| PostToolUse | Run formatter, linter or tests after every edit |
| Stop | Refuse to finish while tests fail |

Rule of thumb: if it must happen every time, make it a hook. If it is guidance, put it in instructions.

Note that hooks are also an attack surface: a malicious repo can ship hook configuration that runs code when the agent starts.

### 3.12 Permission and sandbox layers

Defense in depth, from outermost to innermost:

```text
1. Static rules        allow / ask / deny per tool, command pattern, path or domain
2. Classifier          a second model judges whether an action is safe (Claude Code auto mode, Codex Auto-review)
3. Human approval      the person confirms risky actions
4. OS sandbox          filesystem and network isolation (Seatbelt on macOS, bubblewrap or Landlock on Linux)
5. Environment         container or VM, least-privilege tokens, no production credentials
```

Layers 1 to 3 decide whether an action runs. Layers 4 and 5 limit the damage when the first three are fooled, which prompt injection can do.

### 3.13 Failure modes explained by the internals

| Symptom | Internal cause | Mitigation |
|---|---|---|
| Forgets earlier decisions | Compaction dropped detail; context rot | Memory files, smaller tasks, fresh sessions |
| Declares "done" too early | No objective stopping check | Stop hooks, explicit "done means" criteria |
| Edits tests to make them pass | Optimizing the visible signal | Lock test files, review test diffs separately |
| Loops on the same failing fix | Same context produces the same reasoning | Rewind, add a new hint, switch model or subagent |
| Invents APIs or packages | Generation from patterns, not lookup | Require docs fetch, lockfiles, existence checks |
| Follows instructions found in files | Instructions and data share one channel | Sandbox, deny rules, review untrusted inputs |
| Session gets slow and expensive | Bulky tool results resent every turn | Truncation, clearing, subagents, compaction |

---

## 4. Shared Standards

| Standard | Purpose | Governance |
|---|---|---|
| **AGENTS.md** | Project-level instructions for coding agents: build commands, conventions, rules | Agentic AI Foundation (Linux Foundation) |
| **MCP** (Model Context Protocol) | Connects agents to tools, data and services through one protocol | Agentic AI Foundation (Linux Foundation) |
| **Agent Skills** (`SKILL.md`) | Folders of instructions and scripts loaded on demand | Open standard (agentskills.io), adopted across vendors |

**Teaching point:** one AGENTS.md plus a `skills/` folder in the repo makes the same project work consistently across Codex, Cursor and OpenCode. For Claude Code, add a one-line `CLAUDE.md` that imports it (`@AGENTS.md`).

### Example AGENTS.md

```markdown
# Project: invoice-service

## Stack
- Python 3.12, FastAPI, SQLAlchemy 2.x, pytest
- Do not add new dependencies without asking.

## Commands
- Install: `uv sync`
- Test: `uv run pytest -q`
- Lint: `uv run ruff check . && uv run mypy src`

## Rules
- Write or update tests before changing behavior.
- Run tests and lint after every change; do not report done while anything fails.
- Never edit files under `migrations/` by hand.
- Never print or log secrets; secrets live in `.env`, which must not be read.

## Done means
- All tests pass, lint is clean, and the diff contains no unrelated changes.
```

---

## 5. Prompt and Context Engineering Patterns

Most agent failures come from context, not wording. The context window fills quickly and quality degrades as it fills. Give the agent the right information, a way to check itself, and a clean slate per task.

| Pattern | What to do | Where it lives in agentic tools |
|---|---|---|
| **Role prompting** | State who the agent is acting as and for whom | AGENTS.md or CLAUDE.md, custom agents and modes |
| **Constraint framing** | Specify language version, libraries, edge cases and non-goals up front | AGENTS.md "Stack" and "Rules" sections |
| **Chain of thought** | Ask for reasoning and a plan before code | Plan mode (Claude Code), plan agent (OpenCode), goal or plan prompts (Codex, Cursor) |
| **Context injection** | Point the agent at the relevant files, docs and examples | `@file` mentions, links, skills, MCP resources |
| **Iterative refinement** | Correct and steer the current session rather than restarting blindly | Steering while the agent works, side chats, rewind or checkpoints |
| **Verification criteria** | Give concrete input/output examples or tests the agent must pass | Test files, "Done means" section, hooks that run tests |

### Weak vs strong prompt

Weak:

```text
Write a function to validate emails.
```

Strong:

```text
Add validate_email(addr: str) -> bool to src/validation.py.
Constraints: Python 3.12, standard library only, no regex libraries.
Cases: "user@example.com" -> True, "invalid" -> False, "user@.com" -> False,
"a@b.co" -> True, "" -> False.
First add these cases to tests/test_validation.py and confirm they fail.
Then implement, run the tests, and stop when all pass and ruff is clean.
```

The strong version specifies location, signature, constraints, examples, a test-first order, and a stopping condition.

### Session hygiene

- One task per session. Start fresh when switching tasks.
- When a session drifts, rewind to before the mistake instead of piling on corrections.
- Keep instruction files short. Include only what the agent cannot infer from the code: commands, non-obvious conventions, gotchas.

---

## 6. Code Generation and Testing Patterns

| Pattern | Prompt shape | Watch for |
|---|---|---|
| **Scaffold generation** | High-level spec plus stack and structure constraints | Unrequested dependencies, boilerplate bloat |
| **Function completion** | Signature plus docstring plus examples; agent fills the body | Edge cases not covered by the examples |
| **Test generation** | Target behavior, edge cases, and coverage goal in the prompt | Tests that assert current (buggy) behavior |
| **Explain and document** | "Document the public API of module X; keep examples runnable" | Docs that describe intended rather than actual behavior |
| **Bug diagnosis** | Stack trace plus relevant files; ask for root cause, minimal repro, fix | Fixes that silence the symptom |

### The TDD loop for agents

1. Ask the agent to write tests for the desired behavior. It must not touch the implementation.
2. Run them and confirm they fail for the right reason.
3. Commit the tests.
4. Ask the agent to implement until the tests pass, without modifying the tests.
5. Review the diff. Run the full suite yourself.

### Coverage-driven prompting

```text
Write pytest tests for src/billing/discounts.py targeting at least 90% branch
coverage. Include boundary values, empty inputs, and invalid types.
Run `pytest --cov=src/billing --cov-branch` and report the uncovered lines.
```

### Regression guarding

After a change, ask the agent to review the diff and list tests to add or update. Then run an automated review layer on the PR: Claude Code Code Review, Codex code review, or Cursor Bugbot.

**Key rule:** always run AI-generated tests yourself before committing. A test can pass and still assert the wrong thing.

---

## 7. Agentic Workflows

### 7.1 Plan, Execute, Verify

```text
PLAN      Explore the codebase, read the relevant files, propose a plan
            -> HUMAN CHECKPOINT: approve or edit the plan
EXECUTE   Make changes in small steps, in a branch or worktree
VERIFY    Run tests, lint, type checks (automate with hooks)
            -> loop back to EXECUTE until green
REVIEW    AI review of the diff, then human review
            -> HUMAN CHECKPOINT: merge
```

### 7.2 Non-negotiable human checkpoints

- Approving the plan before large changes.
- Anything touching auth, payments, crypto, data deletion, migrations or infrastructure.
- Adding dependencies.
- Network access to unknown hosts and any action involving credentials.
- Merging to the main branch.

### 7.3 Permission models side by side

| Tool | Cautious setting | Autonomous setting | Extra guardrail |
|---|---|---|---|
| Claude Code | Manual mode | Auto mode (classifier) | Hooks, sandbox, deny rules |
| Codex | Read-only or ask-before-acting profile | Broader profile inside the sandbox | Auto-review agent |
| Cursor | Approve each command | Allowlisted auto-run | Auto-review (SDK), Bugbot |
| OpenCode | `ask` per tool | `allow` per tool or per project | `deny` rules |

### 7.4 Parallelism patterns

- **Best-of-N**: run the same task in several worktrees and keep the best diff (Cursor, Claude Code, Codex).
- **Specialist subagents**: an implementer plus a reviewer on a different model (OpenCode, Claude Code).
- **Fire-and-forget cloud tasks**: delegate well-specified tickets that come back as PRs (Cursor cloud agents, Codex Cloud, Claude Code cloud sessions).

### 7.5 Spec-driven capstone flow

1. Write a one-page spec: goal, constraints, acceptance tests.
2. Have the agent turn it into a step-by-step plan.
3. Human reviews the plan.
4. Implement test-first, one step per commit.
5. AI review, then human review, then merge.

---

## 8. Evals as an Engineering Principle

### 8.1 Why evals

An agent setup is a system with many moving parts: model, harness, effort setting, system prompt, AGENTS.md, skills, MCP tools, hooks. Every change to any of them can improve one behavior and silently break another. Agents are also non-deterministic, so one good run proves little.

Treat agent configuration like code: **no change without a test.** An eval is that test. It gives the agent an input, lets it act, and applies grading logic to the result.

Without evals, decisions rest on impressions, and self-reported productivity is known to be unreliable (section 9.3). With evals, questions like "should we switch to the new model?", "did this AGENTS.md rule help?" or "is Cursor or Claude Code better on *our* repo?" become measurements.

### 8.2 Two kinds of evals

| | Capability evals | Regression evals |
|---|---|---|
| Question | Can the agent do this kind of task at all? | Did a change break something that used to work? |
| Tasks | Hard, frontier tasks; low pass rates expected | Tasks that currently pass |
| When | Choosing tools, models, workflows | Every change to prompts, instruction files, skills, models |
| Goal | Find the ceiling | Keep the floor |

Tasks graduate: once a capability eval passes reliably, move it to the regression suite.

### 8.3 Two loops: evals around the agent, verification inside it

- **Inner loop (inside the agent):** tests, linters, type checks, Stop hooks and review agents are the agent's own evals. They tell it when it is done. Section 3.10 and the "Done means" block in AGENTS.md (section 4) are inline evals.
- **Outer loop (around the agent):** an offline task suite that scores the whole setup across many tasks and trials. It tells *you* whether the setup is improving.

The inner loop makes individual runs correct. The outer loop makes the system better over time.

### 8.4 Building a coding-agent eval suite

1. **Collect 20 to 50 real tasks** from your own history: closed issues with merged fixes, past agent failures, recurring ticket types. Real failures beat synthetic tasks.
2. **Freeze the starting state:** repo URL plus the commit before the fix.
3. **Write the task prompt** the way a developer would actually phrase it (usually the issue text).
4. **Keep a reference solution** for each task. If a competent human cannot solve it from the prompt, the task is broken, not the agent.
5. **Hide the grader:** tests from the real fix are added only *after* the agent finishes, so the agent cannot read or edit them (SWE-bench style).
6. **Run several trials per task** because outcomes vary between runs.
7. **Record everything:** pass/fail, transcript, diff, tokens, cost, wall time, turns, human interventions.

### 8.5 Graders

| Grader | Checks | Strengths | Weaknesses |
|---|---|---|---|
| Code-based | Hidden tests pass, build succeeds, lint clean, test files untouched, diff size, no new dependencies | Deterministic, cheap, fast | Only measures what tests cover |
| Model-based (LLM judge) | Readability, design, adherence to conventions, quality of explanation, rubric scores | Scales to qualitative criteria | Biased and noisy until calibrated |
| Human | Final judgment on a sample; calibrating the LLM judge | Ground truth | Slow, expensive |

Grade the **outcome** (is the repo now correct?) first. Add **trajectory** checks (did it run the tests? did it touch forbidden paths? how many turns?) where process matters. Calibrate any LLM judge against a set of human-labelled examples before trusting it.

### 8.6 Metrics

| Metric | Meaning |
|---|---|
| Resolve rate | Share of tasks where the hidden tests pass |
| pass@k | Probability that at least one of k attempts succeeds. Fits workflows where you pick the best of several runs |
| pass^k | Probability that all k attempts succeed. Measures reliability, which is what unattended agents need |
| Cost per resolved task | Total spend divided by successes. Often a better comparison than raw resolve rate |
| Test-tamper rate | Share of runs that edited existing tests |
| Intervention rate | How often a human had to step in |
| Wall time and turns | Latency and loop efficiency |

pass@k rises with k while pass^k falls. A setup with high pass@3 and low pass^3 looks great in demos and fails in production.

### 8.7 Eval-driven development workflow

```text
1. Baseline      run the suite on the current setup, several trials per task
2. Analyze       read failing transcripts; label each failure (bad plan, wrong file,
                 missed edge case, tool misuse, gave up early, tampered with tests)
3. Change ONE    model, effort, AGENTS.md rule, skill, tool description, hook
4. Re-run        same tasks, same number of trials
5. Compare       resolve rate, pass^k, cost, regressions; check the difference
                 exceeds run-to-run noise
6. Decide        keep or revert; promote newly passing tasks to the regression suite
7. Automate      run the regression suite in CI on every change to agent config
```

Error analysis (step 2) is where most of the value is. Reading 20 failing transcripts usually reveals a fixable pattern faster than any metric.

### 8.8 Minimal eval harness

Runs any headless agent CLI on each task in a fresh checkout, adds hidden tests afterwards, and reports resolve rate, pass^k and tamper rate.

```python
import json, shutil, subprocess, time
from pathlib import Path

# evals/tasks.json:
# [{"id": "t01", "repo": "git@...", "base": "<sha>", "prompt": "...",
#   "test_cmd": "pytest -q tests/test_hidden.py",
#   "hidden": {"evals/hidden/t01/test_hidden.py": "tests/test_hidden.py"}}]
TASKS = json.loads(Path("evals/tasks.json").read_text())

# Adjust flags to each tool's non-interactive / permission docs.
AGENTS = {"claude": ["claude", "-p"], "codex": ["codex", "exec"]}
TRIALS = 3

def sh(cmd, cwd, timeout=1800):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)

def trial(agent, task, k):
    wd = Path(f"/tmp/evals/{agent}/{task['id']}/{k}")
    shutil.rmtree(wd, ignore_errors=True)
    sh(["git", "clone", "-q", task["repo"], str(wd)], cwd="/tmp")
    sh(["git", "checkout", "-q", task["base"]], cwd=wd)
    t0 = time.time()
    sh(AGENTS[agent] + [task["prompt"]], cwd=wd)                      # agent acts
    changed = sh(["git", "diff", "--name-only", task["base"]], cwd=wd).stdout.split()
    tampered = any(f.startswith("tests/") for f in changed)
    for src, dst in task["hidden"].items():                          # grader added after
        (wd / dst).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, wd / dst)
    passed = sh(task["test_cmd"].split(), cwd=wd).returncode == 0
    return {"passed": passed, "tampered": tampered, "secs": round(time.time() - t0)}

for agent in AGENTS:
    runs = {t["id"]: [trial(agent, t, k) for k in range(TRIALS)] for t in TASKS}
    flat = [r for rs in runs.values() for r in rs]
    resolve = sum(r["passed"] for r in flat) / len(flat)
    pass_hat_k = sum(all(r["passed"] for r in rs) for rs in runs.values()) / len(runs)
    tamper = sum(r["tampered"] for r in flat) / len(flat)
    print(f"{agent}: resolve={resolve:.0%} pass^{TRIALS}={pass_hat_k:.0%} tamper={tamper:.0%}")
```

Run it in containers with no real credentials. Agents execute code from the tasks. Extend it with token and cost capture from each tool's JSON output, transcript storage, and an LLM-judge pass for quality.

### 8.9 Pitfalls

- **Contamination:** public repos and benchmarks may be in training data. Prefer private code and tasks newer than the model.
- **Too few tasks or trials:** with 10 tasks, one flaky run moves the score 10 points. Report spread, not just the mean.
- **Flaky tests:** a flaky grader makes every comparison noise. Fix or drop the task.
- **Grading the wrong thing:** passing tests is not the same as a correct solution if coverage is thin. Spot-check diffs by hand.
- **Reward hacking:** agents may edit tests, special-case inputs or skip checks. Hide graders and track tamper rate.
- **Overfitting the suite:** tuning AGENTS.md until the suite passes can encode the test set. Keep a held-out set.
- **Stale suites:** refresh tasks as the codebase and the models change. When everything passes, the suite has stopped measuring.

---

## 9. Evidence: What the Data Says

### 9.1 Benchmarks (read with skepticism)

| Benchmark | What it measures | Recent leaders (BenchLM, October 2026) |
|---|---|---|
| SWE-bench Pro | Real repository issues, harder and less contaminated than older SWE-bench sets | Claude Opus 5.5 at 89.9%, then Sonnet 5.5 and Fable 5.1 around 81% |
| Terminal-Bench 2.0 | Multi-step tasks in real terminal environments | GPT-5.5 at 82%, then GPT-5.3 Codex and GPT-5.4 |

How to read them:

- Rankings change with the benchmark, the harness, the effort setting and the aggregator.
- Some variants are already saturated (top entries near 99%), and successor versions such as Terminal-Bench 2.1 keep appearing.
- The harness is part of the result. The same model scores differently in different agents.
- The real test is your codebase. Build a small internal eval from your own past tickets (section 8).

### 9.2 Capability trend

METR's Time Horizon 1.1 (January 2026) measures how long a task, in expert-human time, an agent can complete with 50% reliability. Since 2023 that horizon has doubled roughly every 4.3 months. The strongest model measured reached a 50% horizon of at least 16 hours, but its 80% horizon was only about 3 hours.

Teaching point: agents can now attempt long tasks, but reliability drops sharply with task length. This is why checkpoints matter.

### 9.3 Productivity

- METR's productivity study (February 2026 update): developers returning from METR's earlier study had an estimated 18% speedup with AI, and newly recruited developers about 4%. Both confidence intervals cross zero.
- METR considers the data a likely lower bound. Many developers refused to work without AI, and 30 to 50% withheld tasks they did not want to do unassisted.
- A METR survey of 349 technical workers found a median self-reported 1.4 to 2x increase in the value of their work, with METR cautioning that self-reports overestimate.
- Takeaway: speedups are likely real but hard to measure, and self-reported gains are unreliable. Measure outcomes (cycle time, defect rates), not feelings.

### 9.4 Skill formation

- In an Anthropic randomized trial, 52 developers learned an unfamiliar Python library (Trio). Those with AI assistance scored about 50% on a mastery quiz versus about 67% for those coding by hand.
- High scorers who used AI used it to understand, not just to produce. They asked follow-up questions, requested explanations, and asked conceptual questions.
- Takeaway: use AI as a thinking partner when learning. Ask "why" and "explain", and write the critical parts yourself.

### 9.5 Trust (Stack Overflow Developer Survey 2026)

- About two thirds of respondents use coding assistants or agents.
- 48% trust AI output only when they can easily verify it. Only 6.6% trust it for important decisions.
- Only 24% say their employer has published approved tools or formal AI guidance.

---

## 10. Security and Responsible Use

### 10.1 The threat model

Coding agents combine three things: access to private code and secrets, exposure to untrusted content (repos, issues, web pages, dependencies), and the ability to act (shell, network, git push). Prompt injection turns untrusted text into actions.

### 10.2 Real attack patterns from 2026

| Pattern | What happened |
|---|---|
| Config files as attack surface | At least 8 prompt-injection CVEs across Copilot, Claude Code, Cursor, Amazon Q and Codex in one year, all via instructions hidden in config files or code comments |
| Trust-prompt abuse ("TrustFall") | A malicious repo spawned an MCP server as soon as the user accepted the folder-trust prompt; the tools tested defaulted to "Trust" |
| Issue-title injection ("Clinejection") | A crafted GitHub issue title hijacked an AI triage bot and led to a compromised npm package, live for about eight hours |
| Worms in agent config | A 2026 npm/PyPI worm hit 170+ packages and persisted through coding-agent hooks and editor auto-run tasks |
| Guardrail evasion | Researchers reported adversarial agents bypassing autonomous-mode safety classifiers in most trials |
| Ecosystem scale | Coding agents make up more than half of the agentic projects tracked by OWASP and carry many of the security advisories |

### 10.3 Defensive checklist

- Treat unknown repos, issues, PR comments, web pages and dependency READMEs as untrusted input.
- Review `.claude/`, `.cursor/`, `.codex/`, `.opencode/`, `.mcp.json`, `AGENTS.md` and hooks in any repo before trusting the folder.
- Enable sandboxing. Prefer cautious permission modes on unfamiliar code.
- Keep secrets out of the working tree and out of the agent's environment. Use deny rules for `.env` and credential paths.
- Pin and review MCP servers, skills and plugins like any other dependency.
- Run CI agents with least-privilege tokens. Never give an agent push access to main.
- Verify that every package an agent adds actually exists and is the one you intended (hallucinated package names get squatted).

### 10.4 IP and copyright

- In most jurisdictions, purely AI-generated material lacks copyright protection without meaningful human authorship. Human selection, arrangement and modification matter.
- Check your tool's license terms, data-retention settings and IP indemnity, especially for enterprise plans.
- Watch for verbatim reproduction of licensed code. Use duplication and license scanners in CI.

### 10.5 When not to use AI (or use it only with heavy review)

- Security-critical logic: auth, crypto, access control.
- Regulated domains where you must explain and certify every line.
- Novel algorithm design, where the model has no patterns to draw from.
- Learning a new technology, where delegation erodes the skill you need for oversight.

---

## 11. Hands-on Exercise Plan

All exercises use the starter repo (section 12). Each lists the goal, the steps, and a "done when" check. Participants use their own tool unless an exercise says otherwise; pairs with different tools compare results at the end of each exercise.

### Session 1

**E0. Setup check (15 min)**
- Goal: everyone has a working agent before content starts.
- Steps: clone the starter repo; run the test command; ask your agent "Explain the structure of this repo and how to run the tests."
- Done when: tests run and the agent produced a correct summary.

**E1. Primitives (20 min, sections 1.1)**
- Goal: feel tokens and sampling directly.
- Steps: paste a 30-line function and a 30-line English paragraph into a tokenizer viewer and compare token counts; run "Write a Python function that parses ISO dates" three times at low temperature and three times at high temperature (API playground or your tool's model settings); note differences.
- Done when: you can explain why code costs more tokens per line and why outputs vary between runs.

**E2. The ladder (20 min, section 1.2)**
- Goal: experience the same task at three rungs.
- Steps: implement `slugify(text: str) -> str` in `exercises/e2/` three times: (a) write the signature and docstring, let autocomplete fill it; (b) ask in chat and paste the answer in; (c) ask the agent to implement it and make `tests/test_slugify.py` pass. Record time, edits needed, and test result for each.
- Done when: your table of time and correctness for the three rungs is posted to the shared sheet.

**E3. Inside the loop (20 min, section 3)**
- Goal: see the ReAct loop as data, not magic.
- Steps: with an Anthropic API key, run the minimal agent from section 3.3 on `exercises/e3/` and print every tool call. Without a key, run your own tool on the same task and open its transcript or verbose view and its context-usage display.
- Done when: you have labelled each step as Thought, Action or Observation, and noted how much context the task used.

**E4. Prompt patterns (20 min, section 5)**
- Goal: practice the five patterns.
- Steps: pick five real tasks from your own work or `exercises/e4/tasks.md`; write one prompt per task using at least three patterns overall (role, constraints, chain of thought, context injection, iterative refinement); run them; swap one prompt with your pair and run it in their tool.
- Done when: for each prompt you noted what made it effective or ineffective.

**E5. Persisted context (25 min, sections 4, 5)**
- Goal: move prompt patterns into files.
- Steps: write an AGENTS.md for the starter repo (stack, commands, rules, done means); re-run one E4 prompt with and without it and compare; run a small feature request in plan mode, review and edit the plan, then execute.
- Done when: your AGENTS.md is committed and you can name one behavior it changed.

### Session 2

**E6. Scaffold and complete (25 min, section 6)**
- Goal: generate structure, then fill details under constraints.
- Steps: from the spec in `exercises/e6/spec.md`, scaffold a small service; then write a signature, docstring and three input/output examples for one function and let the agent implement it.
- Done when: the scaffold runs, and the function passes the provided examples without dependencies you did not approve.

**E7. TDD and coverage (25 min, section 6)**
- Goal: run the agent test-first.
- Steps: in `exercises/e7/`, ask for tests only and confirm they fail; commit them; ask for the implementation without touching tests; then ask for tests that raise branch coverage to 90% and run the coverage report yourself.
- Done when: tests are green, coverage target is met, and `git diff` shows no edits to the committed tests.

**E8. Lab: two hidden bugs (30 min, section 6)**
- Goal: the syllabus lab.
- Steps: in `exercises/e8/`, a 30-line function contains two known bugs. Have the agent generate a test suite, use it to identify both bugs, apply fixes, and confirm all tests pass. Then run the instructor's hidden tests.
- Done when: both bugs are fixed and the hidden tests pass. Bonus: have a second agent or subagent on a different model review the fix.

**E9. Diagnose and guard (20 min, section 6)**
- Goal: root cause analysis and regression guarding.
- Steps: paste the stack trace in `exercises/e9/trace.txt` and ask for root cause, minimal repro and fix; apply it; then ask the agent to review `git diff` and list tests that should be added or updated; add them. If your tool has a review feature, run it on the diff.
- Done when: the fix has a regression test that fails without the fix.

**E10. Mini eval (20 min, section 8)**
- Goal: measure instead of guess.
- Steps: run the harness in `evals/` (section 8.8) on 3 prepared tasks with 2 trials each; add one rule to AGENTS.md (for example "always run the full test suite before finishing"); run again; post resolve rate, pass^2 and tamper rate to the shared table.
- Done when: the class table shows results per tool and per configuration, and you can say whether your rule helped beyond noise.

### Session 3

**E11. Smells, refactor, document (20 min, sections 6, 7)**
- Goal: safe, verified refactoring.
- Steps: in `exercises/e11/legacy.py`, ask the agent to list code smells ranked by severity and fix effort; confirm tests are green; fix only the top smell; confirm tests are still green; generate the module's README section and check it against the code.
- Done when: tests are green before and after, and the diff contains only the intended refactor.

**E12. Plan, Execute, Verify with guardrails (25 min, sections 7, 3.11, 3.12)**
- Goal: build the human-in-the-loop system, not just use it.
- Steps: add a deny rule for `.env` and a guardrail that runs tests automatically (a hook where your tool supports it, otherwise a "done means" rule plus test command); run the multi-step task in `exercises/e12/task.md` with two explicit human checkpoints (plan approval, final diff); if your tool supports parallel attempts, run two and pick the better diff.
- Done when: the guardrail visibly fired at least once, and you approved or rejected at both checkpoints.

**E13. Security drill (20 min, section 10)**
- Goal: see prompt injection happen in a safe environment.
- Steps: open `exercises/e13-untrusted/` in a sandbox with cautious permissions and no real credentials; ask the agent to "fix the failing test"; watch what it tries to do; then inspect README, AGENTS.md, config folders and MCP settings to find the planted instruction; write down the hardening steps that would have stopped it.
- Done when: you found the injection and listed at least three defenses from section 10.3.

**E14. Responsible use check (10 min, sections 9, 10)**
- Goal: apply judgment, not rules of thumb.
- Steps: in pairs, classify the six scenarios in `exercises/e14/scenarios.md` as "use AI", "use with heavy review" or "avoid", with a one-line reason; then open your tool's settings and record its data retention and training settings.
- Done when: your classifications and settings are posted to the shared sheet.

**E15. Capstone (35 min, section 7.5)**
- Goal: one feature end to end using everything from the day.
- Steps: pick a feature from `exercises/capstone/backlog.md`; write a one-page spec with acceptance tests; have the agent produce a plan; approve it; implement test-first; run an AI review of the diff; open a PR with a short description of what the AI did and what you verified.
- Done when: the PR is open, tests pass, and the description lists your verification steps. This PR is part of the final evaluation.

---

## 12. Lab Setup Checklist

### Before the training day (participants)

- [ ] Git, a recent Node.js, and Python with `uv` or `pip` installed.
- [ ] At least one tool installed and signed in: Cursor, Codex (ChatGPT desktop app or CLI), Claude Code, or OpenCode. Run it once on any folder to confirm it works.
- [ ] For OpenCode, an API key from at least one provider (Anthropic requires an API key here, not a consumer subscription).
- [ ] Optional for E3: an Anthropic API key to run the minimal agent from section 3.3.
- [ ] Access to the starter repo confirmed (clone it once).

### Before the training day (instructor)

- [ ] Starter repo with the AGENTS.md from section 4 and an `exercises/` folder: `e2` (slugify tests), `e3` (failing test), `e4/tasks.md`, `e6/spec.md`, `e7`, `e8` (two-bug function plus hidden tests), `e9/trace.txt`, `e11/legacy.py`, `e12/task.md`, `e14/scenarios.md`, `capstone/backlog.md`.
- [ ] An `evals/` folder with 3 prepared tasks, hidden tests and the harness from section 8.8.
- [ ] A separate throwaway repo `e13-untrusted` with a planted, harmless injection (for example an instruction to create a marker file or call a dummy URL). No real credentials anywhere.
- [ ] A shared sheet for posting exercise results (E2, E10, E14) and capstone PR links.
- [ ] Pairing plan that mixes tools.
- [ ] Usage budgets set. Agent sessions consume far more tokens than chat, and several platforms bill by usage.
- [ ] Sandboxing enabled and cautious permission modes as the default for all exercises.
- [ ] A fallback: a spare machine or cloud dev environment with all four tools installed for anyone whose setup fails in E0.

---

## 13. Sources

**Official documentation**

- Claude Code docs and best practices: https://code.claude.com/docs/en/best-practices.md
- Claude Code changelog: https://code.claude.com/docs/en/changelog
- Codex docs and changelog: https://learn.chatgpt.com/codex
- Cursor release notes: https://cursor.com/docs/release-notes
- Cursor cloud agents update: https://cursor.com/changelog/08-19-26
- OpenCode v2 docs: https://opencode.ai/v2/docs/
- OpenCode releases: https://github.com/anomalyco/opencode/releases

**Research and data**

- METR, Time Horizon 1.1: https://metr.org/blog/2026-1-29-time-horizon-1-1/
- METR, developer productivity update: https://metr.org/blog/2026-02-24-uplift-update/
- Anthropic, AI assistance and coding skills: https://www.anthropic.com/research/AI-assistance-coding-skills
- SWE-bench Pro leaderboard (BenchLM): https://benchlm.ai/benchmarks/swe-bench-pro
- Terminal-Bench 2.0 leaderboard (BenchLM): https://benchlm.ai/benchmarks/terminal-bench-2
- Stack Overflow Developer Survey 2026 coverage: https://visualstudiomagazine.com/articles/2026/10/06/stack-overflow-2026-survey-vs-code-leads-visual-studio-takes-third.aspx

**Security**

- OWASP findings on prompt injection in agentic AI: https://www.helpnetsecurity.com/2026/06/11/owasp-prompt-injection-ai-security-failures/
- TrustFall: https://www.securityweek.com/ai-coding-agents-could-fuel-next-supply-chain-crisis/
- CSA note on prompt injection in CI/CD agents: https://labs.cloudsecurityalliance.org/research/csa-research-note-claude-code-github-action-prompt-injection/

**Agent internals**

- ReAct (Yao et al., 2022): https://arxiv.org/abs/2210.03629
- Claude tool use and stop reasons: https://platform.claude.com/docs/de/api/handling-stop-reasons
- Anthropic, Building effective agents: https://www.anthropic.com/engineering/building-effective-agents
- Anthropic, Effective context engineering for AI agents: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic, Writing effective tools for agents: https://www.anthropic.com/engineering/writing-tools-for-agents
- Anthropic, Equipping agents for the real world with Agent Skills: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Anthropic, Code execution with MCP: https://www.anthropic.com/engineering/code-execution-with-mcp

**Evals**

- Anthropic, Demystifying evals for AI agents: https://anthropic.com/engineering/demystifying-evals-for-ai-agents
- SWE-bench (hidden-test methodology): https://www.swebench.com

**Standards**

- Agent Skills: https://agentskills.io
- AGENTS.md: https://agents.md
- Model Context Protocol: https://modelcontextprotocol.io
