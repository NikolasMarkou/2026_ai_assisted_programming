"""Demo 12: count the writing tics of an agent-written document. The count is a floor.

Usage: python3 demos/d12_tic_counter.py [README.md]
Without an argument the built-in sample text is counted. Standard library only.
"""
import collections
import re
import sys

SAMPLE = """# Overview
## Overview of the service
The service is fast, not slow. Most of the work happens in the queue.
## Overview of the queue
We chose a queue rather than a thread pool. This is why it scales.
## Setup
It is not just a cache, it is a store. The majority of requests hit the cache.
"""
text = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else SAMPLE
heads = [m.group(2).split()[0].lower()
         for m in re.finditer(r"^(#{1,4})\s+(.*\S)", text, re.M)]
print("heading first words:", collections.Counter(heads).most_common(3))
TICS = {
    "', not X' tail": r",\s+not\s+[a-z]",
    "'X rather than Y'": r"\brather than\b",
    "'not just X'": r"\bnot just\b",
    "proportion words": r"\b(most|mostly|largely|majority|bulk of)\b",
    "'This is why' closers": r"\bThis is why\b",
}
counts = {name: len(re.findall(pattern, text, re.I)) for name, pattern in TICS.items()}
for name, count in counts.items():
    print(f"{name:26}", count)
print("NOTE: each pattern is a floor. Read what it cannot see.")

# Hidden check (not shown)
if len(sys.argv) == 1:
    assert heads == ["overview", "overview", "overview", "setup"]
    assert list(counts.values()) == [1, 1, 1, 2, 1]
