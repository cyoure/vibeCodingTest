import os
import tempfile
import unittest

from todo.models import Todo, STATUS_DONE, STATUS_TODO
from todo.storage import Storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.tmp_dir.name, "todos.json")
        self.storage = Storage(self.file_path)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_load_returns_empty_list_when_file_missing(self):
        self.assertEqual(self.storage.load(), [])

    def test_save_and_load_round_trip(self):
        todos = [
            Todo(id=1, title="빨래하기"),
            Todo(id=2, title="청소하기", status=STATUS_DONE),
        ]
        self.storage.save(todos)

        loaded = self.storage.load()

        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].title, "빨래하기")
        self.assertEqual(loaded[0].status, STATUS_TODO)
        self.assertEqual(loaded[1].status, STATUS_DONE)

    def test_load_returns_empty_list_when_file_corrupted(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write("이건 JSON이 아님")

        self.assertEqual(self.storage.load(), [])

    def test_load_migrates_legacy_done_boolean_data(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        legacy_data = (
            '[{"id": 1, "title": "빨래하기", "done": false}, '
            '{"id": 2, "title": "청소하기", "done": true}]'
        )
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(legacy_data)

        loaded = self.storage.load()

        self.assertEqual(loaded[0].status, STATUS_TODO)
        self.assertEqual(loaded[1].status, STATUS_DONE)


if __name__ == "__main__":
    unittest.main()
