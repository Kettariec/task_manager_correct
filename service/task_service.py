from typing import Optional
from models.task import Task
from repository.base_repository import BaseRepository
from service.base_service import BaseService


class TaskService(BaseService):
    def __init__(self, repository: BaseRepository):
        self.repository = repository
        self.tasks = self.repository.load_tasks()

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.repository.save_tasks(self.tasks)

    def edit_task(self, task_id: int, **updates):
        for task in self.tasks:
            if task.id == task_id:
                task.title = updates.get("title", task.title)
                task.description = updates.get("description", task.description)
                task.category = updates.get("category", task.category)
                task.deadline = updates.get("deadline", task.deadline)
                task.priority = updates.get("priority", task.priority)
                task.status = updates.get("status", task.status)
                self.repository.save_tasks(self.tasks)
                return True
        return False

    def delete_task(self, task_id: int):
        task = self.repository.get_by_id(task_id)
        if not task:
            return False
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.repository.save_tasks(self.tasks)
        return True

    def get_task_by_id(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def list_tasks(self, category: Optional[str] = None):
        if category:
            return [task for task in self.tasks if task.category == category]
        return self.tasks
