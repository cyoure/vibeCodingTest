from todo.models import Todo, STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE, VALID_STATUSES
from todo.storage import Storage


class TodoService:
    """할 일 추가/조회/상태 전환/삭제/수정에 대한 비즈니스 로직을 담당한다."""

    def __init__(self, storage: Storage):
        self.storage = storage

    def add(self, title: str) -> Todo:
        title = title.strip()
        if not title:
            raise ValueError("제목은 비어 있을 수 없습니다.")

        todos = self.storage.load()
        next_id = max((t.id for t in todos), default=0) + 1
        todo = Todo(id=next_id, title=title, status=STATUS_TODO)
        todos.append(todo)
        self.storage.save(todos)
        return todo

    def list_all(self) -> list[Todo]:
        return self.storage.load()

    def start(self, todo_id: int) -> Todo:
        return self.move(todo_id, STATUS_IN_PROGRESS)

    def complete(self, todo_id: int) -> Todo:
        return self.move(todo_id, STATUS_DONE)

    def move(self, todo_id: int, status: str) -> Todo:
        if status not in VALID_STATUSES:
            raise ValueError(f"올바르지 않은 상태입니다: {status}")
        return self._set_status(todo_id, status)

    def _set_status(self, todo_id: int, status: str) -> Todo:
        todos = self.storage.load()
        todo = self._find(todos, todo_id)
        todo.status = status
        self.storage.save(todos)
        return todo

    def update(self, todo_id: int, new_title: str) -> Todo:
        new_title = new_title.strip()
        if not new_title:
            raise ValueError("제목은 비어 있을 수 없습니다.")

        todos = self.storage.load()
        todo = self._find(todos, todo_id)
        todo.title = new_title
        self.storage.save(todos)
        return todo

    def delete(self, todo_id: int) -> Todo:
        todos = self.storage.load()
        todo = self._find(todos, todo_id)
        todos.remove(todo)
        self.storage.save(todos)
        return todo

    @staticmethod
    def _find(todos: list[Todo], todo_id: int) -> Todo:
        for todo in todos:
            if todo.id == todo_id:
                return todo
        raise ValueError(f"id {todo_id}에 해당하는 할 일이 없습니다.")
