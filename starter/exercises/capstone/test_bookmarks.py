import io
import tempfile
import unittest
from pathlib import Path

import bookmarks


def run(path, *argv):
    """Run the command line on a file; return (exit code, printed text)."""
    out = io.StringIO()
    code = bookmarks.main(["--file", str(path), *argv], out)
    return code, out.getvalue()


class Library(unittest.TestCase):
    def test_add_gives_increasing_ids(self):
        items = []
        first = bookmarks.add(items, "https://a.example", "A")
        second = bookmarks.add(items, "https://b.example", "B", ["x"])
        self.assertEqual((first["id"], second["id"]), (1, 2))
        self.assertEqual(second["tags"], ["x"])

    def test_remove(self):
        items = []
        bookmarks.add(items, "https://a.example", "A")
        self.assertTrue(bookmarks.remove(items, 1))
        self.assertFalse(bookmarks.remove(items, 1))
        self.assertEqual(items, [])

    def test_ids_are_not_reused_after_a_removal_in_the_middle(self):
        items = []
        for name in "abc":
            bookmarks.add(items, f"https://{name}.example", name)
        bookmarks.remove(items, 2)
        self.assertEqual(bookmarks.add(items, "https://d.example", "d")["id"], 4)

    def test_save_and_load_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "marks.json"
            self.assertEqual(bookmarks.load(path), [])
            items = []
            bookmarks.add(items, "https://a.example", "A", ["t"])
            bookmarks.save(path, items)
            self.assertEqual(bookmarks.load(path), items)

    def test_format_item(self):
        item = {"id": 3, "url": "https://a.example", "title": "A", "tags": ["x", "y"]}
        self.assertEqual(bookmarks.format_item(item), "3. A <https://a.example> [x, y]")
        item["tags"] = []
        self.assertEqual(bookmarks.format_item(item), "3. A <https://a.example>")


class CommandLine(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = Path(self.folder.name) / "marks.json"

    def tearDown(self):
        self.folder.cleanup()

    def test_add_list_remove(self):
        added = run(self.path, "add", "https://a.example", "A")
        self.assertEqual(added, (0, "saved 1\n"))
        run(self.path, "add", "https://b.example", "B", "--tag", "x", "--tag", "y")
        self.assertEqual(run(self.path, "list")[1],
                         "1. A <https://a.example>\n2. B <https://b.example> [x, y]\n")
        self.assertEqual(run(self.path, "remove", "1"), (0, "removed 1\n"))
        self.assertEqual(run(self.path, "list")[1], "2. B <https://b.example> [x, y]\n")

    def test_remove_missing_id_exits_1(self):
        self.assertEqual(run(self.path, "remove", "9"), (1, "no bookmark 9\n"))


if __name__ == "__main__":
    unittest.main()
