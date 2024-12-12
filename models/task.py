from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    category: str = ""
    deadline: str = ""
    priority: str = ""
    status: str = "Не выполнена"

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'Task':
        return Task(**data)

    @staticmethod
    def validate_date(date_str: str) -> bool:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
