from models.task import Task
import pytest
from repository.json_repository import JSONRepository
from service.task_service import TaskService


@pytest.fixture
def mock_repository(mocker):
    mock_repo = mocker.Mock(spec=JSONRepository)
    mock_repo.load_tasks.return_value = []
    return mock_repo


def test_add_task(mock_repository):
    service = TaskService(mock_repository)
    task = Task(id=1, title="New Task")
    service.add_task(task)
    assert len(service.tasks) == 1
    assert service.tasks[0].title == "New Task"
    mock_repository.save_tasks.assert_called_once()


def test_edit_task(mock_repository):
    task = Task(id=1, title="Old Task")
    mock_repository.load_tasks.return_value = [task]
    service = TaskService(mock_repository)
    service.edit_task(1, title="Updated Task")
    assert service.tasks[0].title == "Updated Task"
    mock_repository.save_tasks.assert_called_once()


def test_edit_nonexistent_task(mock_repository):
    service = TaskService(mock_repository)
    result = service.edit_task(999, title="Nonexistent Task")
    assert result is False


def test_delete_task(mock_repository):
    task = Task(id=1, title="Task to delete")
    mock_repository.load_tasks.return_value = [task]
    service = TaskService(mock_repository)
    service.delete_task(1)
    assert len(service.tasks) == 0
    mock_repository.save_tasks.assert_called_once()


def test_delete_nonexistent_task(mock_repository):
    service = TaskService(mock_repository)
    mock_repository.get_by_id.return_value = None
    result = service.delete_task(999)
    assert result is False
