from abc import ABC, abstractmethod
from models.task import Task
from typing import List


class BaseRepository(ABC):
    @abstractmethod
    def load_tasks(self):
        pass

    @abstractmethod
    def save_tasks(self, tasks: List[Task]):
        pass

    @abstractmethod
    def add(self, task: Task):
        pass

    @abstractmethod
    def list(self, category: str = None):
        pass

    @abstractmethod
    def update(self, task: Task):
        pass

    @abstractmethod
    def delete(self, task_id: int):
        pass

    @abstractmethod
    def get_by_id(self, task_id: int):
        pass
