# Guardrail examples for E12, one per tool

The config shapes below were checked against vendor documentation on 2026-10-21. They
were NOT run against the real tools on the build machine. Test each one in your own tool
before you trust it. A key name may have changed since the check.

Two scripts do the work for every tool (standard library only, no packages):

- `deny_env.py` reads one JSON event on standard input. It exits 2 (block, with a message
  on standard error) when a file path or a shell command names a `.env` file, and 0
  otherwise. It blocks too when the event cannot be read.
- `run_tests.py` runs `python3 -m unittest -q`. It exits 2 with the last lines of the
  output when the tests fail. With `--followup` it is a Cursor stop hook (see below).

Both are guardrails. Neither is a security boundary. A command that builds the file name at
run time (`cat .e[n]v`, or a Python script that opens the file) passes `deny_env.py`.
That is what the sandbox is for (E13).

## Claude Code

File: `claude_settings.json` in this folder. Copy it to `.claude/settings.json` and copy
the 2 scripts to `.claude/hooks/`. It has 3 parts:

- `permissions.deny` with `Read(./.env)`. Claude Code enforces this rule; the model does not.
  It also covers `cat .env` typed in the shell tool, but not a script that opens the
  file itself. `Read(./.env.*)` follows the documented pattern rules and is untested.
- A `PreToolUse` hook on `Read|Bash`: exit 2 blocks the call before permission rules run.
- A `PostToolUse` hook on `Edit|Write`: exit 2 shows the test output to the agent. The
  edit has already happened.

Exit 1 only warns and does not block. Headless `claude -p` runs project hooks without a
trust question unless `--bare` or `--setting-sources user` is used.

## Cursor

`.cursor/hooks.json` (the `version` key is required):

```json
{
  "version": 1,
  "hooks": {
    "beforeReadFile": [
      {"command": "python3 .cursor/hooks/deny_env.py", "failClosed": true}
    ],
    "beforeShellExecution": [
      {"command": "python3 .cursor/hooks/deny_env.py", "matcher": "\\.env",
       "failClosed": true}
    ],
    "stop": [
      {"command": "python3 .cursor/hooks/run_tests.py --followup", "loop_limit": 2}
    ]
  }
}
```

Plus a `.cursorignore` file with the lines `.env` and `.env.*`. Cursor says the terminal
and MCP tools are not covered by `.cursorignore`, which is why the shell hook is there.
Exit 2 blocks. Any other non-zero exit lets the action through unless `failClosed` is
set. The `stop` hook sends `followup_message` to the agent as the next message, and
`loop_limit` caps it. The page lists no way for an `afterFileEdit` hook to send a result
back, so the tests run at `stop`. Cursor CLI only: `.cursor/cli.json` takes
`{"permissions": {"deny": ["Read(.env*)", "Shell(rm)"]}}`. Whether the editor reads
that file is not documented. Hooks in `cursor-agent` runs are not documented either.

## Codex

`.codex/hooks.json` has the same shape as the Claude Code file:

```json
{
  "hooks": {
    "PreToolUse": [
      {"matcher": "Bash",
       "hooks": [{"type": "command", "command": "python3 .codex/hooks/deny_env.py"}]}
    ],
    "PostToolUse": [
      {"matcher": "apply_patch|Edit|Write",
       "hooks": [{"type": "command", "command": "python3 .codex/hooks/run_tests.py",
                  "timeout": 120}]}
    ]
  }
}
```

A deny rule is a permission profile in `$HOME/.codex/config.toml` (or `.codex/config.toml`,
loaded only in a trusted project). It is documented as beta:

```toml
default_permissions = "guarded"

[permissions.guarded.filesystem]
":minimal" = "read"

[permissions.guarded.filesystem.":workspace_roots"]
"." = "write"
"**/*.env" = "deny"
```

A command rule goes in `.codex/rules/default.rules`:

```text
prefix_rule(pattern=["rm", "-rf"], decision="forbidden", justification="no delete")
```

Codex runs a hook only after you review and trust it with `/hooks`; editing the script
asks again. Whether a relative command path works from every folder is not documented.
Check the rule with `codex execpolicy check`. Behaviour of hooks under `codex exec` when
the hook is not trusted is not documented.

## OpenCode

`opencode.json` already denies the `read` tool on `.env` files by default. This makes it
explicit and asks before any shell command except the ones you allow:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "read": {"*": "allow", "*.env": "deny", "*.env.*": "deny"},
    "shell": {"*": "ask", "rm *": "deny"}
  }
}
```

Which key an installed version accepts for the shell rule (`shell` or the older `bash`)
is not settled: check your version. OpenCode hooks are JavaScript plugins that run inside OpenCode.
The scripts above are shell commands, so they do not apply. A plugin in `.opencode/plugins/guard.js` blocks by
throwing:

```js
export const Guard = async () => ({
  "tool.execute.before": async (input, output) => {
    if (input.tool === "read" && output.args.filePath.includes(".env")) {
      throw new Error("Do not read .env files")
    }
  },
})
```

No hook that feeds failing tests back to the agent is documented. Use the "done means"
rule below, or a `tool.execute.after` plugin, which is untested here.

## When your tool has no hook: a "done means" rule

Put this in `AGENTS.md` (Cursor, Codex and OpenCode read it) and keep the retry cap:

```text
## Done means
- Run `python3 -m unittest -q` after every edit and paste the last line of the output.
- Never read or print `.env`.
- If the tests are still red after 2 fix attempts, stop and tell me what you tried.
```

A rule in a file is read by the model and can be missed. A hook is run by the tool every
time. Use the rule only where no hook exists, and check the result with `check_done.py`.
