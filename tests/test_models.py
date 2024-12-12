from models.task import Task


def test_task_to_dict():
    task = Task(id=1, title="Test Task")
    assert task.to_dict() == {
        "id": 1,
        "title": "Test Task",
        "description": "",
        "category": "",
        "deadline": "",
        "priority": "",
        "status": "Не выполнена",
    }


def test_task_from_dict():
    data = {
        "id": 1,
        "title": "Test Task",
        "description": "Description",
        "category": "Category",
        "deadline": "2023-12-31",
        "priority": "High",
        "status": "In Progress",
    }
    task = Task.from_dict(data)
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Description"
    assert task.category == "Category"
    assert task.deadline == "2023-12-31"
    assert task.priority == "High"
    assert task.status == "In Progress"


def test_task_validate_date():
    assert Task.validate_date("2023-12-31") is True
    assert Task.validate_date("2023-31-12") is False
