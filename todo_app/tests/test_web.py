import os
import tempfile
import unittest

from web.app import create_app


class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        file_path = os.path.join(self.tmp_dir.name, "todos.json")
        app = create_app(data_file=file_path)
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_index_shows_empty_columns(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("할 일 (0)".encode(), response.data)
        self.assertIn("진행중 (0)".encode(), response.data)
        self.assertIn("완료 (0)".encode(), response.data)

    def test_add_creates_todo_and_redirects(self):
        response = self.client.post("/add", data={"title": "빨래하기"})
        self.assertEqual(response.status_code, 302)

        response = self.client.get("/")
        self.assertIn("빨래하기".encode(), response.data)

    def test_add_with_empty_title_shows_flash_message(self):
        self.client.post("/add", data={"title": "   "})

        response = self.client.get("/")
        self.assertIn("오류".encode(), response.data)

    def test_move_to_in_progress_column(self):
        self.client.post("/add", data={"title": "빨래하기"})
        response = self.client.post("/move/1", data={"status": "in_progress"})
        self.assertEqual(response.status_code, 302)

        response = self.client.get("/")
        self.assertIn("진행중 (1)".encode(), response.data)
        self.assertIn("할 일 (0)".encode(), response.data)

    def test_move_to_done_column(self):
        self.client.post("/add", data={"title": "빨래하기"})
        self.client.post("/move/1", data={"status": "done"})

        response = self.client.get("/")
        self.assertIn("완료 (1)".encode(), response.data)

    def test_move_back_to_todo_column(self):
        self.client.post("/add", data={"title": "빨래하기"})
        self.client.post("/move/1", data={"status": "done"})
        self.client.post("/move/1", data={"status": "todo"})

        response = self.client.get("/")
        self.assertIn("할 일 (1)".encode(), response.data)
        self.assertIn("완료 (0)".encode(), response.data)

    def test_move_with_invalid_status_shows_flash_message(self):
        self.client.post("/add", data={"title": "빨래하기"})
        self.client.post("/move/1", data={"status": "not-a-status"})

        response = self.client.get("/")
        self.assertIn("오류".encode(), response.data)
        self.assertIn("할 일 (1)".encode(), response.data)

    def test_delete_removes_todo(self):
        self.client.post("/add", data={"title": "빨래하기"})
        self.client.post("/delete/1")

        response = self.client.get("/")
        self.assertNotIn("빨래하기".encode(), response.data)


if __name__ == "__main__":
    unittest.main()
