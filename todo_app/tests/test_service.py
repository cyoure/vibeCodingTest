import os
import tempfile
import unittest

from todo.service import TodoService
from todo.storage import Storage
from todo.models import STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE


class TestTodoService(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        file_path = os.path.join(self.tmp_dir.name, "todos.json")
        self.service = TodoService(Storage(file_path))

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_add_creates_todo_with_incrementing_id(self):
        first = self.service.add("빨래하기")
        second = self.service.add("청소하기")

        self.assertEqual(first.id, 1)
        self.assertEqual(second.id, 2)
        self.assertEqual(first.status, STATUS_TODO)

    def test_add_rejects_empty_title(self):
        with self.assertRaises(ValueError):
            self.service.add("   ")

    def test_list_all_returns_added_todos(self):
        self.service.add("빨래하기")
        self.service.add("청소하기")

        todos = self.service.list_all()

        self.assertEqual(len(todos), 2)

    def test_start_moves_to_in_progress(self):
        todo = self.service.add("빨래하기")

        updated = self.service.start(todo.id)

        self.assertEqual(updated.status, STATUS_IN_PROGRESS)
        self.assertEqual(self.service.list_all()[0].status, STATUS_IN_PROGRESS)

    def test_start_raises_for_missing_id(self):
        with self.assertRaises(ValueError):
            self.service.start(999)

    def test_complete_moves_to_done(self):
        todo = self.service.add("빨래하기")

        updated = self.service.complete(todo.id)

        self.assertEqual(updated.status, STATUS_DONE)
        self.assertEqual(self.service.list_all()[0].status, STATUS_DONE)

    def test_complete_raises_for_missing_id(self):
        with self.assertRaises(ValueError):
            self.service.complete(999)

    def test_move_back_to_todo(self):
        todo = self.service.add("빨래하기")
        self.service.complete(todo.id)

        updated = self.service.move(todo.id, STATUS_TODO)

        self.assertEqual(updated.status, STATUS_TODO)

    def test_move_rejects_invalid_status(self):
        todo = self.service.add("빨래하기")

        with self.assertRaises(ValueError):
            self.service.move(todo.id, "not-a-status")

    def test_update_changes_title(self):
        todo = self.service.add("빨래하기")

        updated = self.service.update(todo.id, "빨래 개기")

        self.assertEqual(updated.title, "빨래 개기")
        self.assertEqual(self.service.list_all()[0].title, "빨래 개기")

    def test_update_rejects_empty_title(self):
        todo = self.service.add("빨래하기")

        with self.assertRaises(ValueError):
            self.service.update(todo.id, "   ")

    def test_update_raises_for_missing_id(self):
        with self.assertRaises(ValueError):
            self.service.update(999, "새 제목")

    def test_delete_removes_todo(self):
        todo = self.service.add("빨래하기")

        self.service.delete(todo.id)

        self.assertEqual(self.service.list_all(), [])

    def test_delete_raises_for_missing_id(self):
        with self.assertRaises(ValueError):
            self.service.delete(999)


if __name__ == "__main__":
    unittest.main()
