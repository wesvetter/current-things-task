import importlib.util
import unittest
from pathlib import Path


def load_plugin():
    path = Path(__file__).with_name("current-task.60s.py")
    spec = importlib.util.spec_from_file_location("current_task", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SelectCurrentTaskTest(unittest.TestCase):
    def setUp(self):
        self.plugin = load_plugin()

    def test_picks_first_today_task_in_the_target_area(self):
        tasks = [
            {"title": "Personal one", "area": "Personal", "tags": []},
            {"title": "Work one", "area": "Work", "tags": []},
            {"title": "Work two", "area": "Work", "tags": []},
        ]
        chosen = self.plugin.select_current_task(tasks, {
            "target_area_name": "Work",
            "hidden_label": "Hidden",
        })
        self.assertEqual(chosen["title"], "Work one")

    def test_includes_tasks_whose_area_comes_from_a_project(self):
        tasks = [
            {"title": "Inbox", "area": "Personal", "tags": []},
            {"title": "In a work project", "area": "Work", "tags": []},
        ]
        chosen = self.plugin.select_current_task(tasks, {
            "target_area_name": "Work",
            "hidden_label": "Hidden",
        })
        self.assertEqual(chosen["title"], "In a work project")

    def test_skips_tasks_with_the_hidden_label(self):
        tasks = [
            {"title": "Secret", "area": "Work", "tags": ["Hidden"]},
            {"title": "Visible", "area": "Work", "tags": ["Chore"]},
        ]
        chosen = self.plugin.select_current_task(tasks, {
            "target_area_name": "Work",
            "hidden_label": "Hidden",
        })
        self.assertEqual(chosen["title"], "Visible")

    def test_null_area_keeps_today_order(self):
        tasks = [
            {"title": "Anything", "area": "Personal", "tags": []},
            {"title": "Later", "area": "Work", "tags": []},
        ]
        chosen = self.plugin.select_current_task(tasks, {
            "target_area_name": None,
            "hidden_label": "Hidden",
        })
        self.assertEqual(chosen["title"], "Anything")

    def test_returns_none_when_nothing_matches(self):
        chosen = self.plugin.select_current_task([], {
            "target_area_name": "Work",
            "hidden_label": "Hidden",
        })
        self.assertIsNone(chosen)

    def test_truncates_long_titles(self):
        self.assertEqual(
            self.plugin.truncate_title("abcdefghijklmnopqrstuvwxyz", 20),
            "abcdefghijklmnopqrst...",
        )

    def test_parse_today_output(self):
        payload = "\x1e".join([
            "Buy milk\x1fFamily\x1fChore, Hidden",
            "Ship it\x1fWork\x1f",
        ])
        tasks = self.plugin.parse_today_output(payload)
        self.assertEqual(tasks, [
            {"title": "Buy milk", "area": "Family", "tags": ["Chore", "Hidden"]},
            {"title": "Ship it", "area": "Work", "tags": []},
        ])
        self.assertIsNone(self.plugin.parse_today_output("NOT_RUNNING"))
        self.assertEqual(self.plugin.parse_today_output(""), [])


if __name__ == "__main__":
    unittest.main()
