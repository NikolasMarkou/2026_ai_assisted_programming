# E4 Prompt patterns: 5 tasks

Pick 5 tasks: these, or real ones from your own work. Write one prompt per task. Across the 5
prompts use at least 3 of these patterns: role, constraints, chain of thought (ask for a plan
before code), context injection (name the files, docs or examples), iterative refinement
(correct the current session), verification criteria (examples or tests the answer must pass).

Run the prompts in your tool. Swap one prompt with your pair and run it in their tool.
For each prompt write down what made it effective or ineffective.

## The tasks

1. Input validation. A function `create_user(name, email, age)` in a web service stores whatever
   it receives. Add validation for the three fields and return error messages a client can
   show. The project has unit tests for the happy path only.

2. Slow report. A nightly job builds a CSV report from 2 million rows and takes 40 minutes.
   You have the job script and a profiler output that shows 70 percent of the time in one loop.
   Make it faster without changing the CSV format.

3. Unreadable stack trace. A deployment fails with a 60 line Python stack trace that ends in
   `KeyError: 'region'` inside a library you do not own. Find the cause in your own code and
   propose the smallest fix.

4. Rename across a codebase. The word `customer` must become `client` in function names,
   database column names and the API documentation of a service with 300 files. Existing
   database rows must keep working.

5. Flaky test. A test fails about 1 run in 10 on the CI server and never on your laptop.
   You have the test file, the CI log of one failed run and the code under test.
   Find out why and fix the cause. Do not add a retry.

## Notes to write for each prompt

- Which patterns did you use?
- What did the agent get wrong or skip?
- What would you add to the prompt next time?
