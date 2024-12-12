from cli import CLI
from models.task import Task
import pytest
from repository.json_repository import JSONRepository
from service.task_service import TaskService


@pytest.fixture
def cli_instance(mocker):
    mock_repo = mocker.Mock(spec=JSONRepository)
    mock_service = TaskService(mock_repo)
    cli = CLI()
    cli.service = mock_service
    return cli, mock_service


def test_run_cli_exit(cli_instance, monkeypatch):
    cli, service = cli_instance
    inputs = iter(["5"])

    def mock_input(prompt):
        return next(inputs)
    monkeypatch.setattr("builtins.input", mock_input)
    try:
        cli.run()
    except Exception as e:
        pytest.fail(f"CLI завершился с исключением: {e}")


def test_add_task_cli(cli_instance, monkeypatch, mocker):
    cli, service = cli_instance
    service.tasks = []
    inputs = iter([
        "2",
        "Test Task",
        "Test Description",
        "Test Category",
        "2024-12-31",
        "3",
        "5"
    ])

    def mock_input(prompt):
        return next(inputs)
    monkeypatch.setattr("builtins.input", mock_input)
    cli.run()
    assert len(service.tasks) == 1
    assert service.tasks[0].title == "Test Task"


def test_list_tasks_cli(cli_instance, monkeypatch, mocker):
    cli, service = cli_instance
    service.tasks = [
        Task(id=1, title="Task 1"),
        Task(id=2, title="Task 2"),
    ]
    inputs = iter(["1", "5"])

    def mock_input(prompt):
        try:
            return next(inputs)
        except StopIteration:
            return "5"
    monkeypatch.setattr("builtins.input", mock_input)
    cli.run()
    assert len(service.tasks) == 2
    assert service.tasks[0].title == "Task 1"
    assert service.tasks[1].title == "Task 2"


def test_edit_task_cli(cli_instance, monkeypatch, mocker):
    cli, service = cli_instance
    task = Task(id=1, title="Old Task")
    service.tasks = [task]
    inputs = iter([
        "3",
        "1",
        "Updated Task",
        "Updated Description",
        "Updated Category",
        "2024-12-31",
        "1",
        "2",
        "5"
    ])

    def mock_input(prompt):
        try:
            return next(inputs)
        except StopIteration:
            return "5"

    monkeypatch.setattr("builtins.input", mock_input)
    cli.run()
    assert len(service.tasks) == 1
    assert service.tasks[0].title == "Updated Task"


def test_delete_task_cli(cli_instance, monkeypatch, mocker):
    cli, service = cli_instance
    task = Task(id=1, title="Task to delete")
    service.tasks = [task]
    inputs = iter([
        "4",
        "1",
        "5"
    ])

    def mock_input(prompt):
        return next(inputs)
    monkeypatch.setattr("builtins.input", mock_input)
    cli.run()
    assert len(service.tasks) == 0


def test_invalid_input(cli_instance, monkeypatch):
    cli, service = cli_instance
    inputs = iter([
        "invalid",
        "5"
    ])

    def mock_input(prompt):
        return next(inputs)

    monkeypatch.setattr("builtins.input", mock_input)
    try:
        cli.run()
    except ValueError:
        pass
