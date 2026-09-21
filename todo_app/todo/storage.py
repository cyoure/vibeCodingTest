import json
import os

from todo.models import Todo


class Storage:
    """JSON 파일 읽기/쓰기만 담당한다. 비즈니스 규칙은 포함하지 않는다."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> list[Todo]:
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
        return [Todo.from_dict(item) for item in raw]

    def save(self, todos: list[Todo]) -> None:
        dir_name = os.path.dirname(self.file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in todos], f, ensure_ascii=False, indent=2)
