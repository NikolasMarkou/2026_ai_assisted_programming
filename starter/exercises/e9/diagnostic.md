# E9 Diagnostic: which part failed

Use these 4 questions in order when an agent gets something wrong. Stop at the first
question you answer with the stated answer.

1. Was the information or tool it needed in front of it? If no, the failed part is knowledge and tools.
2. Did an action reach beyond the boundary you set? If yes, the failed part is the sandbox.
3. Was the loop wrong: no check run, stopped early, lost context, repeated itself, bad plan? If yes, the failed part is the harness.
4. Were the inputs, the boundary and the loop all right, and the result still wrong? If yes, the failed part is the model.

Reading the questions on a transcript:

- Question 1, in front of it: the agent had the file or fact when it was in its context
  window or its instruction files. In an eval transcript that is an `ACT: read` line for
  the code file. An agent that writes a file it never read had nothing in front of it.
- Question 2, the boundary: a path the task did not let the agent reach, such as a file
  outside the working folder (the line `left outside the workspace` lists it), the network
  or a credential. A protected test inside the folder is not the boundary. The line
  `protected paths touched` is the reward-hacking case, and the key labels it model.
- Two failures look alike: a new `src/slugify.py` and a new `../slugify.py`, each ending
  in a "fixed" claim. The first is inside the folder and the code was never read, so
  question 1 gives knowledge and tools. The second follows a read and the header lists the
  file outside the folder, so question 2 gives sandbox.

The 4 labels, in the order of the questions:

| Label | What it covers |
|---|---|
| knowledge and tools | what the agent could know (instruction files, repository, docs) and the tools it was given |
| sandbox | the boundary: files, network and credentials the agent could reach |
| harness | the loop around the model: checks, stop conditions, context, plan, permissions |
| model | the next-token prediction itself: wrong logic, invented facts, reward hacking |

## Label one failure

Fill one row for each wrong answer your agent gives in this exercise.

| What went wrong | Q1 | Q2 | Q3 | Q4 | Failed part |
|---|---|---|---|---|---|
| | | | | | |
