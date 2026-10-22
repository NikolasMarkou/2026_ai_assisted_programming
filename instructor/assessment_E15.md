# E15 final assessment

10 items, 10 minutes, on your own, no tool. Single choice: write one letter. Short answer:
write at most 2 sentences. Each item has a tag with the part of the agent it tests:
model, harness, sandbox, knowledge and tools, or all (it tests the whole assembly). Hand out
everything above the line "ANSWER KEY". Keep the key.

## Items

1. [part: model] [topic: sampling] You run the same prompt twice and get two different
   functions. Which statement explains it?
   - A. The loop of the agent has a bug.
   - B. The model picks each next token from a probability distribution, so runs differ
     unless the sampling is fixed.
   - C. The sandbox changed between the runs.
   - D. The instruction file was loaded twice.

2. [part: knowledge and tools] [topic: diagnostic] An agent wrote tests by reading the
   buggy function. The tests pass and the bug is still there. You never gave it the
   rules the function should follow. Which part failed, using the four questions?

3. [part: harness] [topic: retry cap] The tests are still red after the agent's second fix
   attempt on a step. What happens next under the rule of the day?

4. [part: harness] [topic: self-report] The agent ends with "all tests pass". Who must run
   the check before you accept it, and why?

5. [part: sandbox] [topic: scope] A sandbox allows writes anywhere inside the project folder
   and blocks the network. An injected line makes the agent create a file in the project
   folder. Does the sandbox stop it? Say why.

6. [part: knowledge and tools] [topic: instruction files] Name one way an instruction file
   such as AGENTS.md goes wrong over time, and one check that detects it.

7. [part: all] [topic: eval noise] Your eval of 3 tasks with 2 trials each shows that a new
   rule raises the pass rate by 17 points. What do you do before you believe it?
   - A. Believe it: 17 points is a large gap.
   - B. Run more tasks and more seeds and look at the spread, because in a small eval a
     rule that does nothing can still show a gap of 15 points or more.
   - C. Stop using evals.
   - D. Raise the temperature and run once more.

8. [part: all] [topic: eval tamper] Four scripted runs all pass the visible tests: one edits
   the expected value in a test, one special-cases the test input, one adds an untracked
   module that shadows the real one, and one really fixes the bug. Which check separates the
   real fix from the other 3?
   - A. A list of the files in `git diff` whose names start with `tests/`.
   - B. Hidden tests that the agent cannot reach.
   - C. The agent's own summary of what it changed.
   - D. Running the visible tests a second time.

9. [part: harness] [topic: injection] A deny rule blocks the command `touch INJECTION_FOLLOWED.txt`
   but lets `touch INJECTION_"FOLLOWED".txt` through. Name two defences that stop both
   spellings.

10. [part: all] [topic: responsible use] A team wants an agent to write the dose calculation
    of a regulated medical device. What is your answer, and what may the agent do instead?

---

# ANSWER KEY (do not hand out)

Scoring: 1 point per item, 10 in total. For a short answer give the point when the answer
names the idea in the key; the wording does not matter. Each line ends with the evidence.

1. **B.** Sampling is a draw from a probability distribution (demo: `exercises/e1_sampler`
   shows low and high temperature on a bigram model).
2. **Knowledge and tools.** Question 1 of the diagnostic: the rules were not in front of it,
   and tests written from the code pass on the code (demo d2: 4 of 4 agent tests pass, 0 of 3
   spec tests).
3. **It stops and shows you** what it tried and what failed; it does not make a third
   attempt (`exercises/e12/pev.py`, the cap is 2 fix attempts). Accept "the person decides:
   revert, fix by hand or change the task".
4. **The harness or you run the check; the agent does not.** A self-report is not evidence
   (demo d9: a summary said healthy for 9 days while the raw rows said otherwise).
5. **No.** The write is inside the allowed area. The OS sandbox and least-privilege
   credentials limit reach beyond the folder and do not limit a write inside it (E13, marker
   files).
6. **Stale commands or paths** (a make target that is gone, a folder that moved) **caught by
   a lint that checks every command and path exists** (`exercises/e5/lint_agents_md.py`,
   demo d11). Accept "rules that contradict the code" with a check that reads the code.
7. **B.** In demo d8, with 3 tasks and 2 trials, a rule that did nothing showed a gap of 15
   points or more in 78% of simulated evals; at 30 tasks and 5 trials it was 1%.
8. **B.** Demo d3: the diff-name check flags only the edited test; `git status` also sees the
   untracked module; only the hidden tests fail all 3 cheats and pass the real fix.
9. **Any 2 of:** human approval (a person reads the command), a hook that allows only known
   commands, an allow list in the permission rules. The OS sandbox and the credentials do
   not stop a write in the folder (E13 answer key).
10. **Avoid generating it.** Every line must be explained and certified, so a person writes
    and certifies it. The agent may help with tests, documentation and a review checklist
    that a person checks (E14 scenario 5).

Part coverage: model 1 item (1); harness 3 items (3, 4, 9); sandbox 1 item (5); knowledge
and tools 2 items (2, 6); all 3 items (7, 8, 10).
