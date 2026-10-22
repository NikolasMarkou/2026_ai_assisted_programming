import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path

import tasklist


class TaskListTest(unittest.TestCase):
    def test_add_numbers_tasks_from_1(self):
        tasks = []
        tasklist.add(tasks, "Write tests")
        tasklist.add(tasks, "Ship it")
        self.assertEqual([t["id"] for t in tasks], [1, 2])

    def test_add_rejects_an_empty_title(self):
        with self.assertRaises(ValueError):
            tasklist.add([], "   ")

    def test_complete_marks_the_task_done(self):
        tasks = []
        tasklist.add(tasks, "Write tests")
        tasklist.complete(tasks, 1)
        self.assertTrue(tasks[0]["done"])

    def test_complete_unknown_id_raises(self):
        with self.assertRaises(KeyError):
            tasklist.complete([], 3)

    def test_render_marks_done_tasks(self):
        tasks = []
        tasklist.add(tasks, "One")
        tasklist.add(tasks, "Two")
        tasklist.complete(tasks, 2)
        self.assertEqual(tasklist.render(tasks), "[ ] 1 One\n[x] 2 Two")

    def test_command_line_round_trip(self):
        with tempfile.TemporaryDirectory() as folder, \
                contextlib.redirect_stdout(io.StringIO()):
            path = str(Path(folder) / "tasks.json")
            os.environ["TASKLIST_FILE"] = path
            self.assertEqual(tasklist.main(["add", "Write tests"]), 0)
            self.assertEqual(tasklist.main(["done", "1"]), 0)
            self.assertTrue(tasklist.load(path)[0]["done"])
            self.assertEqual(tasklist.main(["bogus"]), 1)

    def test_add_stores_a_due_date(self):
        tasks = []
        tasklist.add(tasks, "Write tests", due="2026-11-01")
        self.assertEqual(tasks[0]["due"], "2026-11-01")

    def test_add_rejects_a_bad_due_date(self):
        for bad in ("11/01/2026", "2026-13-01", "2026-1-5", "tomorrow"):
            with self.assertRaises(ValueError):
                tasklist.add([], "Write tests", due=bad)

    def test_render_shows_the_due_date_only_when_there_is_one(self):
        tasks = []
        tasklist.add(tasks, "One", due="2026-11-01")
        tasklist.add(tasks, "Two")
        self.assertEqual(tasklist.render(tasks),
                         "[ ] 1 One (due 2026-11-01)\n[ ] 2 Two")

    def test_overdue_is_open_and_strictly_before_today(self):
        tasks = []
        cases = (("early", "2026-10-31"), ("same day", "2026-11-02"),
                 ("late", "2026-12-01"), ("none", None), ("done", "2026-10-01"))
        for title, due in cases:
            tasklist.add(tasks, title, due=due)
        tasklist.complete(tasks, 5)
        late = tasklist.overdue(tasks, "2026-11-02")
        self.assertEqual([t["title"] for t in late], ["early"])

    def test_a_file_written_before_due_dates_still_loads(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tasks.json"
            path.write_text('[{"id": 1, "title": "Old", "done": false}]')
            self.assertEqual(tasklist.render(tasklist.load(path)), "[ ] 1 Old")

    def test_command_line_due_and_overdue(self):
        with tempfile.TemporaryDirectory() as folder, \
                contextlib.redirect_stdout(io.StringIO()) as out:
            os.environ["TASKLIST_FILE"] = str(Path(folder) / "tasks.json")
            self.assertEqual(tasklist.main(["add", "Late", "--due", "2026-10-01"]), 0)
            self.assertEqual(tasklist.main(["add", "Soon", "--due", "2026-12-01"]), 0)
            self.assertEqual(tasklist.main(["add", "Bad", "--due", "soon"]), 1)
            out.truncate(0)
            out.seek(0)
            self.assertEqual(
                tasklist.main(["list", "--overdue", "--today", "2026-11-02"]), 0)
            self.assertEqual(out.getvalue().strip(), "[ ] 1 Late (due 2026-10-01)")
            self.assertEqual(len(tasklist.load(os.environ["TASKLIST_FILE"])), 2)


if __name__ == "__main__":
    unittest.main()
