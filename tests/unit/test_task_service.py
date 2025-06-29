import pytest
from unittest.mock import MagicMock, patch
from app.application.services.task_service import TaskService
from app.infrastructure.repositories.task_repository import TaskRepository
from app.domain.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.models.task import Task
from app.domain.exceptions import NotFoundError
from datetime import datetime
from app.domain.schemas.user import UserResponseTaskList

@pytest.fixture
def mock_repository():
    """Fixture for a mock of TaskRepository"""
    return MagicMock(spec=TaskRepository)

@pytest.fixture
def task_service(mock_repository):
    """Fixture for the task service with mocked repository"""
    return TaskService(mock_repository)

# Test for task creation
def test_create_task_success(task_service, mock_repository):
    """Test: Successful task creation"""
    # Configuration
    task_data = TaskCreate(
        task="Tarea de prueba",
        description="Descripción de la tarea",
        user_id=1,
        type="personal",
        priority="medium",
        status="pending"
    )

    # Configure mock behavior
    mock_repository.create.return_value = TaskResponse(
        id=1,
        task=task_data.task,
        description=task_data.description,
        created_at=task_data.created_at,
        status=task_data.status,
        user=UserResponseTaskList(id=1, name="Test", surname="User", email="test@example.com"),
        type="personal",
        priority="medium",
        progress=0
    )

    # Execute
    created_task = task_service.create_task(task_data)

    # Verify
    assert created_task.task == "Tarea de prueba"
    assert created_task.description == "Descripción de la tarea"
    assert created_task.status == "pending"
    assert created_task.created_at == task_data.created_at
    assert created_task.status != "done"
    
    # Verify interactions
    mock_repository.create.assert_called_once_with(task_data)

def test_get_task_success(task_service, mock_repository):
    """Test: Get existing task"""
    # Configuration
    task_id = 1
    existing_task = TaskResponse(
        id=task_id,
        task="Tarea existente",
        description="Descripción de la tarea existente",
        due_date=datetime(2025, 7, 1),
        completed=False,
        created_at=datetime.now(),
        user=UserResponseTaskList(id=1, name="Test", surname="User", email="test@example.com"),
        type="personal",
        priority="medium",
        status="pending",
        progress=0
    )

    # Configure mock behavior
    
    mock_repository.get_by_id.return_value = existing_task

    # Execute
    task = task_service.get_task(task_id)

    # Verify
    assert task.task == "Tarea existente"
    assert task.description == "Descripción de la tarea existente"
    assert task.status == "pending"
    
    # Verify interactions
    mock_repository.get_by_id.assert_called_once_with(task_id)

def test_get_task_not_found(task_service, mock_repository):
    """Test: Attempt to get non-existent task"""
    # Configuration
    task_id = 999
    mock_repository.get_by_id.return_value = None

    # Execute and verify exception
    with pytest.raises(NotFoundError) as exc_info:
        task_service.get_task(task_id)
    
    # Verify error message
    assert "Task not found" in str(exc_info.value)
    mock_repository.get_by_id.assert_called_once_with(task_id)

def test_update_task_success(task_service, mock_repository):
    """Test: Successful task update"""
    # Configuration
    task_id = 1
    existing_task = TaskResponse(
        id=task_id,
        task="Tarea original",
        description="Descripción original",
        due_date=datetime(2025, 7, 1),
        completed=False,
        created_at=datetime.now(),
        user=UserResponseTaskList(id=1, name="Test", surname="User", email="test@example.com"),
        type="personal",
        priority="medium",
        status="pending",
        progress=0
    )

    update_data = TaskUpdate(
        task="Tarea actualizada",
        description="Descripción actualizada",
        status="done"
    )

    # Configure mock behavior
    mock_repository.get_by_id.return_value = existing_task
    mock_repository.update.return_value = TaskResponse(
        id=task_id,
        task="Tarea actualizada",
        description="Descripción actualizada",
        created_at=datetime.now(),
        user=UserResponseTaskList(id=1, name="Test", surname="User", email="test@example.com"),
        type="personal",
        priority="medium",
        status="done",
        progress=0
    )

    # Execute
    updated_task = task_service.update_task(task_id, update_data)

    # Verify
    assert updated_task.task == "Tarea actualizada"
    assert updated_task.description == "Descripción actualizada"
    assert updated_task.status == "done"
    
    # Verify interactions
    mock_repository.get_by_id.assert_called_once_with(task_id)
    mock_repository.update.assert_called_once()

def test_delete_task_success(task_service, mock_repository):
    """Test: Successful task deletion"""
    # Configuration
    task_id = 1
    mock_repository.get_by_id.return_value = TaskResponse(
        id=task_id,
        task="Tarea a eliminar",
        description="Descripción",
        due_date=datetime(2025, 7, 1),
        completed=False,
        created_at=datetime.now(),
        user=UserResponseTaskList(id=1, name="Test", surname="User", email="test@example.com"),
        type="personal",
        priority="medium",
        status="pending",
        progress=0
    )

    # Execute
    task_service.delete_task(task_id)

    # Verify
    mock_repository.get_by_id.assert_called_once_with(task_id)
    mock_repository.delete.assert_called_once_with(task_id)
