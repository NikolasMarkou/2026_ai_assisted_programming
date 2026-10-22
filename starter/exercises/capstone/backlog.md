# Capstone backlog

Pick 1 feature. The base app is `bookmarks.py`; its tests are in `test_bookmarks.py` and
pass. Every feature below is small on purpose, because the exercise practises the process.
Each feature has acceptance criteria. Your spec must restate them as tests.

Run the tests from this folder:

```text
python3 -m unittest -q
```

## 1. Tag filter

`list --tag TAG` prints only the bookmarks that have TAG.

- The match is exact on the tag text and does not depend on upper or lower case.
- A tag with no match prints nothing and the exit code is 0.
- `list` without `--tag` prints everything, as it does today.

## 2. Duplicate URLs

`add` refuses a URL that is already saved.

- Two URLs are the same when they match after the scheme and host are written in lower
  case, one trailing `/` is removed and everything from `#` on is removed.
- A duplicate prints `already saved: ID` with the id of the saved bookmark, exits with
  1, and does not change the file.
- A different URL is saved as before.

## 3. Search

`search WORD` prints the bookmarks whose title or URL contains WORD.

- The match does not depend on upper or lower case.
- Bookmarks whose title matches come first, then those where only the URL matches. Inside
  each group the order is by id.
- No match prints nothing and the exit code is 0. Output lines use the `list` format.

## 4. Markdown export

`export --format md` prints the bookmarks as a Markdown list.

- One line per bookmark, in id order: `- [TITLE](URL)`. When the bookmark has tags the line
  ends with a space and the tags in brackets: `- [TITLE](URL) [tag1, tag2]`.
- An empty file prints nothing and the exit code is 0.
- Any other format name is refused with the usual argument error (exit code 2).

## Your process

0. Copy this folder to `capstone_work`. Run `git init -b main`, commit the base app and
   switch to a branch with `git switch -c feature`. A local repository is enough. If
   your git rejects `-b` (older than 2.28), run `git init` and then `git checkout -b main`.
1. Write a one-page spec: goal, constraints, the acceptance tests.
2. Ask the agent for a step-by-step plan. Read it. Approve it or edit it.
3. Implement test-first, one step per commit.
4. Ask for an AI review of the diff. Then read the diff yourself.
5. Fill `PULL_REQUEST_TEMPLATE.md` into a file called `PR_DESCRIPTION.md` and run:

```text
python3 check_capstone.py
```

6. Add the output of `git log main..feature` and `git diff main feature` to the end of
   `PR_DESCRIPTION.md`, then copy `PR_DESCRIPTION.md` and `bookmarks.py` to your folder in
   the shared folder. No remote is needed.
