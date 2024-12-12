from datetime import datetime
from models.task import Task
from repository.json_repository import JSONRepository
from service.task_service import TaskService


class CLI:
    def __init__(self):
        repository = JSONRepository()
        self.service = TaskService(repository)

    def run(self):
        while True:
            print("\nМенеджер задач:")
            print("1. Просмотр задач")
            print("2. Добавить задачу")
            print("3. Изменить задачу")
            print("4. Удалить задачу")
            print("5. Выйти")

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                category = input("Введите категорию или ENTER для всех задач: ").strip()
                tasks = self.service.list_tasks(category if category else None)
                if tasks:
                    for task in tasks:
                        print(task.to_dict())
                else:
                    print("Нет задач для отображения.")

            elif choice == "2":
                title = input("Название задачи: ").strip()
                while not title:
                    print("Название задачи обязательно.")
                    title = input("Название задачи: ").strip()

                description = input("Описание: ").strip()
                category = input("Категория: ").strip()
                deadline = input("Срок (YYYY-MM-DD): ").strip()
                while deadline and not Task.validate_date(deadline):
                    print("Некорректный формат даты. Попробуйте снова.")
                    deadline = input("Срок (YYYY-MM-DD): ").strip()

                priority = input("Приоритет (1-Низкий, 2-Средний, 3-Высокий): ").strip()
                priority = {"1": "Низкий", "2": "Средний", "3": "Высокий"}.get(priority, "Низкий")

                task = Task(
                    id=int(datetime.now().timestamp()),
                    title=title,
                    description=description,
                    category=category,
                    deadline=deadline,
                    priority=priority,
                )
                self.service.add_task(task)
                print("Задача добавлена!")

            elif choice == "3":
                try:
                    task_id = int(input("ID задачи: ").strip())
                    existing_task = self.service.get_task_by_id(task_id)
                    if not existing_task:
                        print("Задача с таким ID не найдена.")
                        continue
                    print("Введите новое значение или нажмите Enter, чтобы сохранить текущее.")
                    title = input(f"Новое название (текущее: {existing_task.title}): ").strip() or existing_task.title
                    description = input(
                        f"Новое описание (текущее: {existing_task.description}): ").strip() or existing_task.description
                    category = input(
                        f"Новая категория (текущая: {existing_task.category}): ").strip() or existing_task.category
                    deadline = input(f"Новый срок (текущий: {existing_task.deadline}, формат YYYY-MM-DD): ").strip()
                    while deadline and not Task.validate_date(deadline):
                        print("Некорректный формат даты. Попробуйте снова.")

                        deadline = input(f"Новый срок (текущий: {existing_task.deadline}, формат YYYY-MM-DD): ").strip()
                    deadline = deadline or existing_task.deadline
                    priority = input(
                        f"Новый приоритет (1-Низкий, 2-Средний, 3-Высокий, текущий: {existing_task.priority}): "

                    ).strip()
                    priority = {"1": "Низкий", "2": "Средний", "3": "Высокий"}.get(priority, existing_task.priority)
                    status = input(
                        f"Новый статус (1-В процессе, 2-Выполнена, текущий: {existing_task.status}): "
                    ).strip()
                    status = {"1": "В процессе", "2": "Выполнена",}.get(status, existing_task.status)
                    updates = {
                        "title": title,
                        "description": description,
                        "category": category,
                        "deadline": deadline,
                        "priority": priority,
                        "status": status,
                    }
                    self.service.edit_task(task_id, **updates)
                    print("Задача обновлена!")

                except ValueError:
                    print("Некорректный ID!")

            elif choice == "4":
                try:
                    task_id = int(input("ID задачи: ").strip())
                    if not self.service.get_task_by_id(task_id):
                        print("Задача с таким ID не найдена.")
                        continue
                    self.service.delete_task(task_id)
                    print("Задача удалена!")
                except ValueError:
                    print("Некорректный ID!")

            elif choice == "5":
                break

            else:
                print("Неверный выбор!")
