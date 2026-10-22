# Day-of checklist (22 October 2026)

Run it top to bottom. Every command runs from the deck folder
(`docs/trainings/2026_ai_assisted_programming`) unless it says `starter/`.

## The evening before

- [ ] Rebuild the venv and run the kit verifier from `build/`. It must print
  `RESULT: N checks, 0 failed`. A red line the night before leaves time to decide what to do:

  ```text
  cd build && make verify-kit
  ```

- [ ] `make` in `build/` and open `slides.pdf`. Page count and footer total as in `content.md`.
- [ ] Copy `slides.pdf` and the whole `starter/` folder to a USB stick. Copy `talk_track.md`
  and this `instructor/` folder to the trainer laptop only. Never put `instructor/hidden/`
  or `instructor/solutions/` on the stick that goes to the room.
- [ ] Three tools signed in on three laptops, each with a usage budget set: one of Cursor,
  Codex, Claude Code, OpenCode per laptop, plus the key for the live API call if you want
  `live_call`. Check that each tool answers one prompt in its own folder.
- [ ] A spare machine with all four tools installed and the `starter/` folder on it.
- [ ] Printed: the sign-in sheet, `assessment_E15.md` without the key, `pairing_plan.md`.

## Morning, before 09:00

- [ ] Venue wifi: open one page. If it fails, switch the trainer laptop to the phone hotspot
  and tell the room that every exercise runs offline.
- [ ] Wifi fallback: the scripted agent, the demos, the eval harness and every check run
  offline. A pair's own tool and the exchange folder below need a connection. If the
  network is down, use the second USB stick below for E10 and copy the pairs' files
  from their laptops yourself (E8, E9 and the capstone).
- [ ] Create the shared sheet from `results_sheet_template.csv` (columns: pair, tool,
  exercise, time, result, note). Share the link on the first slide.
- [ ] Create the exchange folder: a shared folder that every laptop can write to (a cloud
  drive, or the room's chat if no drive works), with 1 subfolder per pair named `pair-NN`.
  Post its link next to the sheet link on the first slide. Pairs put `shipping.py` there
  after E8, `report.py` after E9, and `bookmarks.py` with `PR_DESCRIPTION.md` at the final
  evaluation, each author in a folder of their own inside it. You download each file to
  your laptop and run the hidden tests on that copy.
- [ ] Prepare a second USB stick that holds only a folder named `hidden_evals` (a copy of
  `instructor/hidden/evals`) and nothing else. It is the fallback for E10 when the network
  is down: pairs copy the folder from it into `starter/`.
- [ ] On each laptop: `python3 check_env.py` from `starter/`. It exits 0 when Python is 3.10
  or newer and git is present.
- [ ] Build the sign-in sheet at the door (name, tool, signed in, budget) and make the pairs
  with `pairing_plan.md`.

## REVERIFY sweep (vendor facts can change overnight)

1. Count the markers: every `<!-- REVERIFY -->` in the module files has a row in the
   REVERIFY table in `content.md`. Read each row and open its source key from section 9.1.
2. Re-check these flags on the machine you present from. A flag that no longer appears
   in the help text means the slide or the talk track is stale: say so aloud.

   ```text
   claude --help
   opencode --help
   opencode run --help
   codex --help
   codex exec --help
   cursor-agent --help
   ```

   Look for: Claude Code `--bare`, `--setting-sources`, `--settings`, `--permission-mode`,
   `--allowedTools`; OpenCode `run` `--auto`; Codex `exec` `--sandbox` (and that
   `--full-auto` is gone). Where a tool is not installed, read its page from the source key.
3. Build-machine record, 2026-10-21: `claude --help` (2.1.306) lists `--bare`,
   `--setting-sources`, `--settings`, `--permission-mode` and `--allowedTools`;
   `opencode run --help` (v2.0.32) lists `--auto`; `codex` and `cursor-agent` were not
   installed, so their flags come from the vendor pages only.
4. The first two to retest: the HTTP 400 on a non-default temperature for the Sonnet model
   (ledger N-01) and the FN-09 note (open item 6 in `content.md`).
5. Write the result of each sweep next to the REVERIFY row (checked on, result).

## Where each fallback output lives, and how to run its demo live

Use the live command first. When it fails, show the recorded file and say it is a
recording. Each file is compared byte for byte with a fresh run by `make verify-kit`.

| Fallback file | Run it live from `starter/` |
|---|---|
| fallback_outputs/agent_trace_e3.txt | `python3 agent/minimal_agent.py e3_work` on a copy of `exercises/e3` |
| fallback_outputs/bigram.txt | `python3 exercises/e1_sampler/bigram.py --seed 7` |
| fallback_outputs/bigram_compare.txt | `python3 exercises/e1_sampler/bigram.py --compare` |
| fallback_outputs/cheating_matrix.txt | recorded by `make verify-kit`; no single live command |
| fallback_outputs/d1_agent_loop.txt | `python3 demos/d1_agent_loop.py` |
| fallback_outputs/d2_gate_cannot_fail.txt | `python3 demos/d2_gate_cannot_fail.py` |
| fallback_outputs/d3_tamper.txt | `python3 demos/d3_tamper.py` |
| fallback_outputs/d4_history_leak.txt | `python3 demos/d4_history_leak.py` |
| fallback_outputs/d5_stale_number.txt | `python3 demos/d5_stale_number.py` |
| fallback_outputs/d6_run_the_listings.txt | `python3 demos/d6_run_the_listings.py` |
| fallback_outputs/d7_fooled_model_guard.txt | `python3 demos/d7_fooled_model_guard.py` |
| fallback_outputs/d8_noise.txt | `python3 demos/d8_noise.py` |
| fallback_outputs/d9_green_for_nine_days.txt | `python3 demos/d9_green_for_nine_days.py` |
| fallback_outputs/d10_shell_chain.txt | `python3 demos/d10_shell_chain.py` |
| fallback_outputs/d11_agentsmd_lint.txt | `python3 demos/d11_agentsmd_lint.py` |
| fallback_outputs/d12_tic_counter.txt | `python3 demos/d12_tic_counter.py` |
| fallback_outputs/d13_ignored_setting.txt | `python3 demos/d13_ignored_setting.py` |
| fallback_outputs/e6_third_party_import.txt | `python3 exercises/e6/check_scaffold.py` on a folder with a `requests` import |
| fallback_outputs/e8_hidden_run.txt | in `hidden/e8` run `PYTHONPATH=<pair's exercises/e8> python3 -B -m unittest -q test_hidden`; copy nothing into the pair's folder |
| fallback_outputs/e9_run.txt | in `hidden/e9` run `PYTHONPATH=<pair's exercises/e9> python3 -B -m unittest -q test_hidden`; copy nothing into the pair's folder |
| fallback_outputs/e11_checks.txt | `python3 exercises/e11/check_refactor.py` and `python3 exercises/e11/check_readme.py` in a copy of `exercises/e11` |
| fallback_outputs/e12_guardrails_run.txt | `python3 exercises/e12/check_done.py` in a git copy of `exercises/e12`; the hook cases are in `hooks/README.md` |
| fallback_outputs/e12_pev_never_green.txt | `python3 exercises/e12/pev.py --agent "python3 never_green.py agent" --verify "python3 never_green.py verify"` in a copy of `exercises/e12` |
| fallback_outputs/e13_drill.txt | `python3 agent/injected_agent.py e13_work --deny` then `python3 exercises/e13-untrusted/check_injection.py e13_work`, on a fresh copy each time |
| fallback_outputs/grep_shell_function.txt | `type grep` and `grep -rc Overfull .` in the trainer's agent shell (only that tool) |
| fallback_outputs/harness_run.txt | `python3 evals/harness.py --configs baseline,run_tests_first --trials 3 --seeds 1-5 --no-time --hidden ../instructor/hidden/evals` |
| fallback_outputs/live_call.txt | one live call, needs `ANTHROPIC_API_KEY`; recorded status is NOT RUN |
| fallback_outputs/passk.txt | `python3 evals/passk.py --p 0.8 --k 5` |

## During the day

- [ ] E8 and E9: download `shipping.py` or `report.py` from the pair's subfolder of the
  exchange folder into a scratch folder and run the hidden tests there (table above); the
  tests are not handed out and nothing is copied into the pair's own folder.
- [ ] E10: copy `hidden/evals` into the exchange folder as a folder named `hidden_evals`
  (just before 12:55), or hand round the USB stick. Pairs copy it into `starter/`, add
  `--hidden hidden_evals` and delete it after E10. Give each pair its own block of 5 seeds
  (`--seeds 1-5`, `6-10`, and so on).
- [ ] `evals/flaky_agent.py` holds the labelling key for E10 (`KIND_PART`). That is accepted. Tell pairs to label from the output files.
- [ ] E12 and E13: the hook examples were checked against vendor pages and not run
  against the real tools. Say so before the exercise, and record what a pair finds.
- [ ] E15: use `pairing_plan.md` for the rotation. Print `assessment_E15.md` without
  the key and keep the key. For a capstone, download `bookmarks.py` from the pair's
  subfolder and run, from `hidden/capstone`,
  `PYTHONPATH=<folder with bookmarks.py> python3 -B -m unittest test_hidden.<Class>` for
  the feature the author chose. `PR_DESCRIPTION.md` ends with the output of
  `git log main..feature` and `git diff main feature`.
- [ ] After each exercise, collect results on the shared sheet before the next block starts.

## Who to call

Fill these in before the day; do not look them up on the day.

- Venue IT contact and the wifi password: ______________________
- Venue host for power, projector and room keys: ______________________
- A second trainer or a colleague who can take the spare machine: ______________________
- Billing contact for the tools' usage budgets: ______________________
