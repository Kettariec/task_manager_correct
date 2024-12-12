from models.task import Task
import pytest
from repository.json_repository import JSONRepository


@pytest.fixture
def temp_json_file(tmp_path):
    file = tmp_path / "tasks.json"
    file.write_text("[]", encoding="utf-8")
    return file


def test_load_tasks(temp_json_file):
    repo = JSONRepository(file_path=str(temp_json_file))
    tasks = repo.load_tasks()
    assert tasks == []


def test_save_and_load_tasks(temp_json_file):
    repo = JSONRepository(file_path=str(temp_json_file))
    tasks = [Task(id=1, title="Task 1"), Task(id=2, title="Task 2")]
    repo.save_tasks(tasks)

    loaded_tasks = repo.load_tasks()
    assert len(loaded_tasks) == 2
    assert loaded_tasks[0].title == "Task 1"
    assert loaded_tasks[1].title == "Task 2"


def test_load_tasks_file_not_found():
    repo = JSONRepository(file_path="non_existent.json")
    tasks = repo.load_tasks()
    assert tasks == []


def test_load_tasks_invalid_json(temp_json_file):
    temp_json_file.write_text("{invalid_json}")
    repo = JSONRepository(file_path=str(temp_json_file))
    tasks = repo.load_tasks()
    assert tasks == []
