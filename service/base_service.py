from abc import ABC, abstractmethod
from models.task import Task


class BaseService(ABC):
    @abstractmethod
    def add_task(self, task: Task):
        pass

    @abstractmethod
    def edit_task(self, task_id: int, **updates):
        pass

    @abstractmethod
    def delete_task(self, task_id: int):
        pass

    @abstractmethod
    def get_task_by_id(self, task_id: int):
        pass

    @abstractmethod
    def list_tasks(self, category: str = None):
        pass
