from dataclasses import dataclass, asdict
from datetime import datetime

STATUS_TODO = "todo"
STATUS_IN_PROGRESS = "in_progress"
STATUS_DONE = "done"
VALID_STATUSES = (STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE)


@dataclass
class Todo:
    id: int
    title: str
    status: str = STATUS_TODO
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat(timespec="seconds")

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Todo":
        status = data.get("status")
        if status not in VALID_STATUSES:
            status = STATUS_DONE if data.get("done") else STATUS_TODO

        return Todo(
            id=data["id"],
            title=data["title"],
            status=status,
            created_at=data.get("created_at", ""),
        )
