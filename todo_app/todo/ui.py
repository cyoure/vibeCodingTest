from todo.service import TodoService
from todo.models import STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE

STATUS_LABELS = {
    STATUS_TODO: "할 일",
    STATUS_IN_PROGRESS: "진행중",
    STATUS_DONE: "완료",
}

HELP_TEXT = """\
사용 가능한 명령어:
  add     - 새 할 일 추가
  list    - 할 일 목록 조회
  start   - 할 일을 '진행중' 상태로 변경
  done    - 할 일을 '완료' 상태로 변경
  edit    - 할 일 제목 수정
  delete  - 할 일 삭제
  help    - 명령어 도움말 출력
  exit    - 프로그램 종료
"""


def run(service: TodoService) -> None:
    print("MiniTask CLI에 오신 것을 환영합니다. 'help'를 입력하면 명령어를 볼 수 있습니다.")
    while True:
        command = input("\n> ").strip().lower()

        if command == "add":
            _handle_add(service)
        elif command == "list":
            _handle_list(service)
        elif command == "start":
            _handle_start(service)
        elif command == "done":
            _handle_done(service)
        elif command == "edit":
            _handle_edit(service)
        elif command == "delete":
            _handle_delete(service)
        elif command == "help":
            print(HELP_TEXT)
        elif command == "exit":
            print("프로그램을 종료합니다.")
            break
        elif command == "":
            continue
        else:
            print(f"알 수 없는 명령어입니다: {command} (help 입력 시 도움말 출력)")


def _handle_add(service: TodoService) -> None:
    title = input("할 일 제목: ")
    try:
        todo = service.add(title)
        print(f"추가됨: [{todo.id}] {todo.title}")
    except ValueError as e:
        print(f"오류: {e}")


def _handle_list(service: TodoService) -> None:
    todos = service.list_all()
    if not todos:
        print("등록된 할 일이 없습니다.")
        return
    for todo in todos:
        label = STATUS_LABELS[todo.status]
        print(f"[{label}] {todo.id}. {todo.title}")


def _handle_start(service: TodoService) -> None:
    todo_id = _read_id()
    if todo_id is None:
        return
    try:
        todo = service.start(todo_id)
        print(f"진행중으로 변경됨: [{todo.id}] {todo.title}")
    except ValueError as e:
        print(f"오류: {e}")


def _handle_done(service: TodoService) -> None:
    todo_id = _read_id()
    if todo_id is None:
        return
    try:
        todo = service.complete(todo_id)
        print(f"완료 처리됨: [{todo.id}] {todo.title}")
    except ValueError as e:
        print(f"오류: {e}")


def _handle_edit(service: TodoService) -> None:
    todo_id = _read_id()
    if todo_id is None:
        return
    new_title = input("새 제목: ")
    try:
        todo = service.update(todo_id, new_title)
        print(f"수정됨: [{todo.id}] {todo.title}")
    except ValueError as e:
        print(f"오류: {e}")


def _handle_delete(service: TodoService) -> None:
    todo_id = _read_id()
    if todo_id is None:
        return
    try:
        todo = service.delete(todo_id)
        print(f"삭제됨: [{todo.id}] {todo.title}")
    except ValueError as e:
        print(f"오류: {e}")


def _read_id() -> int | None:
    raw = input("할 일 번호(id): ").strip()
    if not raw.isdigit():
        print("오류: 숫자로 된 id를 입력해야 합니다.")
        return None
    return int(raw)
