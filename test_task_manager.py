import unittest
import tempfile
from pathlib import Path

from task_manager import TaskManager
from utils import valid_task_name, valid_date
from analytics import TaskAnalytics


class TestProject(unittest.TestCase):
    def test_add_task(self):
        with tempfile.TemporaryDirectory() as folder:
            manager = TaskManager(Path(folder) / "tasks.csv")
            self.assertTrue(manager.add_task("Python", "Study", "High", "2026-10-05"))
            self.assertEqual(len(manager.tasks), 1)

    def test_complete_task(self):
        with tempfile.TemporaryDirectory() as folder:
            manager = TaskManager(Path(folder) / "tasks.csv")
            manager.add_task("Python", "Study", "High", "")
            self.assertTrue(manager.complete_task(1))
            self.assertEqual(manager.tasks[0]["status"], "Completed")

    def test_validation(self):
        self.assertTrue(valid_task_name("Python"))
        self.assertFalse(valid_task_name(""))
        self.assertTrue(valid_date("2026-10-05"))
        self.assertFalse(valid_date("05-10-2026"))

    def test_statistics(self):
        tasks = [{
            "id": "1", "task": "Python", "category": "Study", "priority": "High",
            "created_at": "2026-10-01 09:00", "due_date": "2026-10-02",
            "status": "Completed", "completed_at": "2026-10-01 11:00"
        }]
        stats = TaskAnalytics(tasks).statistics()
        self.assertEqual(stats["completed"], 1)
        self.assertEqual(stats["average"], 2.0)
        self.assertEqual(len(stats["completion_array"]), 1)

    def test_filter(self):
        manager = TaskManager()
        manager.add_task("Python", "Study", "High", "")
        manager.add_task("Meeting", "Work", "Low", "")
        result = manager.search_filter("Python", "All", "All")
        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
