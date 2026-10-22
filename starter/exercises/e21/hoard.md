# Hoard: answers you have seen work

Simon Willison's chapter "Hoard things you know how to do" says: "A key asset to develop
as a software professional is a deep collection of answers to questions like this,
accompanied by proof of those answers." The chapter is at
https://simonwillison.net/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/
(page read on 2026-10-22). It is one person's practice, with his own examples.

An entry here has a question, the answer, a command that proves it and the output of
that command. The command must run from the `starter/` folder and exit with status 0. An
answer you cannot run is a note, not a hoard entry.

## Entry 1: keep a number inside a range

Question: how do I keep a discount between 0 and a maximum?
Answer: `max(0, min(percent, MAX_DISCOUNT))`, as written in `clamp_discount()` in
`exercises/e21/agent_pr/cart.py`.
Proof command: `python3 exercises/e21/agent_pr/cart.py --discount 120 2000 500`
Proof output: `discount asked: 120 percent, applied: 50 percent`

## Entry 2: yours

Write one entry about something you saw work today, in the same four lines.

Question:
Answer:
Proof command:
Proof output:
