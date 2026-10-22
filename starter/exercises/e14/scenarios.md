# E14 Responsible use check

Work in pairs.

## Part 1. Classify the 6 scenarios

For each scenario write one label and one line of reason. The labels are:

- use AI: the agent can write it and normal review is enough.
- use with heavy review: the agent can draft it, and a person with the right skill reads
  every line and runs the checks.
- avoid: a person writes it, or the agent only explains and tests.

Ask yourself 3 things: what breaks if it is wrong, can a test or a person tell that it is
wrong, and what do you learn or lose by delegating it?

| # | Scenario | Label | One-line reason |
|---|---|---|---|
| 1 | A script that parses a CSV export from your billing system and prints a monthly summary for the team. Output is easy to check against the CSV. | | |
| 2 | Middleware that validates JWT tokens on every request of a customer-facing API. | | |
| 3 | A database migration that drops 2 columns from a production table with 40 million rows. | | |
| 4 | You must use a library you have never used, next week, and you want to understand it. | | |
| 5 | The dose calculation of a regulated medical device. Every line must be explained and certified. | | |
| 6 | A scheduling algorithm for a problem no one in your team has seen before. There is no reference solution. | | |

## Part 2. Record your tool's data settings

Open the settings of your tool and fill in one row. Write what you see on screen. If you cannot find a setting, write "not found" and ask the instructor.

| Item | Your tool |
|---|---|
| Tool and plan (personal, team, enterprise, API) | |
| Where the data settings are (menu or page) | |
| Is your code kept after the session, and for how long? | |
| Is your code used to train models? Can you turn it off? | |
| Who can see your sessions (you, admins, no one)? | |
| Is there an IP indemnity for generated code on your plan? | |

Settings change by plan and by date. Write the date you checked.

Done when your 6 labels and your settings row are on the shared sheet.
