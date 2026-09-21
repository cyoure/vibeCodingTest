from config import DATA_FILE
from todo.storage import Storage
from todo.service import TodoService
from todo.ui import run


def main() -> None:
    storage = Storage(DATA_FILE)
    service = TodoService(storage)
    run(service)


if __name__ == "__main__":
    main()
