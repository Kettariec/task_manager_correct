import json
from models.task import Task
from repository.base_repository import BaseRepository
from typing import List


class JSONRepository(BaseRepository):
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = file_path

    def load_tasks(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return [Task.from_dict(task) for task in json.load(file)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self, tasks: List[Task]):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in tasks], file, ensure_ascii=False, indent=4)

    def add(self, task):
        self.data.append(task)

    def list(self, category=None):
        if category:
            return [task for task in self.data if task.category == category]
        return self.data

    def update(self, task):
        for i, existing_task in enumerate(self.data):
            if existing_task.id == task.id:
                self.data[i] = task
                return

    def delete(self, task_id):
        self.data = [task for task in self.data if task.id != task_id]

    def get_by_id(self, task_id: int):
        tasks = self.load_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None

