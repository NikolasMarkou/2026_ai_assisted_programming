# Review checklist for a pull request an agent made

Source: Simon Willison, "Agentic Engineering Patterns", chapter "Anti-patterns"
(https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/, page read
on 2026-10-22; his chapters are living documents, so check the page for the current
wording). The chapter has one named anti-pattern, inflicting unreviewed code on
collaborators. His rule is about filing a pull request: "Don't file pull requests with
code you haven't reviewed yourself." The chapter lists four checklist points and
recommends evidence of testing. They are numbered here as five points; the questions
under each are ours.

How to use it: the pull request is in `exercises/e21/agent_pr/` (`pr_text.md` is the
description, `diff.patch` the change, `cart.py` the file after the change). For each
point write yes or no and one line saying why, after "Your answer:".

## 1. It works, and you are confident that it works

His words: "you are confident that it works". Question: which command did you run, and
what did it print? Does a test exist for each behaviour the change adds?

Your answer:

## 2. It is small

His words: "Several small PRs beats one big one". Question: how many files and lines does
the diff change? Would you split it?

Your answer:

## 3. It gives the reviewer context

He lists the goal and linked issues or specs. Question: does the text say what the
change is for, and where the request came from?

Your answer:

## 4. You reviewed the description

His words: "Agents write convincing looking pull request descriptions. You need to review
these too!" Question: is every claim in the text true? Check each one against the diff
and by running it.

Your answer:

## 5. It has evidence of testing

His words: "I recommend including some form of evidence that you've put that extra work
in yourself." Question: for each claim, what is the evidence, and can you see it in the
text or run it?

Your answer:

## Your decision

Would you file this pull request as it is, send it back, or change it first? One line.

Your answer:
