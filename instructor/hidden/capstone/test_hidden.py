"""Hidden acceptance tests for the 4 capstone backlog features (one class each).

Run from this folder, with the author's capstone_work folder on PYTHONPATH, one class
at a time. Never copy this file into the author's folder. For example:
    PYTHONPATH=<capstone_work> python3 -B -m unittest test_hidden.TagFilter
Each class fails on the base app and passes on the reference solution. The seeding
uses only the base `add` command, so the same setup works for every feature.
"""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import bookmarks


def run(path, *argv):
    """Run the command line on a file. Returns (exit code, printed text)."""
    out = io.StringIO()
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            code = bookmarks.main(["--file", str(path), *argv], out)
    except SystemExit as error:
        code = error.code
    return code, out.getvalue()


def ids(text):
    """The ids at the start of each output line."""
    return [line.split(".")[0] for line in text.splitlines()]


class Seeded(unittest.TestCase):
    ROWS = [("https://Py.example/Docs/", "Python docs", ["Python", "docs"]),
            ("https://news.example/a", "Daily news", ["news"]),
            ("https://example.org/python-tips", "Tips", []),
            ("https://blog.example/b", "My PYTHON notes", ["python"])]

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = Path(self.folder.name) / "marks.json"
        for url, title, tags in self.ROWS:
            flags = [x for tag in tags for x in ("--tag", tag)]
            assert run(self.path, "add", url, title, *flags)[0] == 0

    def tearDown(self):
        self.folder.cleanup()


class TagFilter(Seeded):
    def test_only_bookmarks_with_the_tag_in_any_case(self):
        code, text = run(self.path, "list", "--tag", "PYTHON")
        self.assertEqual(code, 0)
        self.assertEqual(ids(text), ["1", "4"])

    def test_tag_with_no_match_prints_nothing(self):
        self.assertEqual(run(self.path, "list", "--tag", "nothing"), (0, ""))

    def test_tag_match_is_exact(self):
        self.assertEqual(run(self.path, "list", "--tag", "pyth"), (0, ""))

    def test_list_without_a_tag_prints_everything(self):
        self.assertEqual(len(run(self.path, "list")[1].splitlines()), 4)


class Duplicates(Seeded):
    def test_same_url_after_normalizing_is_refused(self):
        before = self.path.read_text()
        code, text = run(self.path, "add", "HTTPS://py.EXAMPLE/Docs#intro", "Again")
        self.assertEqual((code, text), (1, "already saved: 1\n"))
        self.assertEqual(self.path.read_text(), before)

    def test_a_different_path_is_saved(self):
        self.assertEqual(run(self.path, "add", "https://py.example/Docs/2", "Two"),
                         (0, "saved 5\n"))

    def test_the_trailing_slash_is_the_only_one_removed(self):
        self.assertEqual(run(self.path, "add", "https://news.example/a/", "A")[0], 1)
        self.assertEqual(run(self.path, "add", "https://news.example/a//", "A")[0], 0)


class Search(Seeded):
    def test_title_matches_first_then_url_matches(self):
        code, text = run(self.path, "search", "python")
        self.assertEqual(code, 0)
        self.assertEqual(ids(text), ["1", "4", "3"])

    def test_no_match_prints_nothing(self):
        self.assertEqual(run(self.path, "search", "zebra"), (0, ""))

    def test_output_uses_the_list_format(self):
        self.assertEqual(run(self.path, "search", "daily")[1],
                         "2. Daily news <https://news.example/a> [news]\n")


class MarkdownExport(Seeded):
    def test_one_line_per_bookmark_with_tags_in_brackets(self):
        code, text = run(self.path, "export", "--format", "md")
        self.assertEqual(code, 0)
        self.assertEqual(text.splitlines(), [
            "- [Python docs](https://Py.example/Docs/) [Python, docs]",
            "- [Daily news](https://news.example/a) [news]",
            "- [Tips](https://example.org/python-tips)",
            "- [My PYTHON notes](https://blog.example/b) [python]"])

    def test_empty_file_prints_nothing(self):
        empty = Path(self.folder.name) / "empty.json"
        self.assertEqual(run(empty, "export", "--format", "md"), (0, ""))

    def test_unknown_format_is_an_argument_error(self):
        self.assertEqual(run(self.path, "export", "--format", "html")[0], 2)


if __name__ == "__main__":
    unittest.main()
