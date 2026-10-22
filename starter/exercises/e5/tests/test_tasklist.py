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


if __name__ == "__main__":
    unittest.main()
