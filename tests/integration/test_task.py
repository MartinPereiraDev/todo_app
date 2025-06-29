from fastapi.testclient import TestClient
from app.infrastructure.database import get_session, Session
from app.models.task import Task, TaskType, TaskPriority, TaskStatus
from app.domain.schemas.user import Role
import pytest
from app.main import app
import os
from app.infrastructure.database import init_db, cleanup_db

# Import Task model for test data
from app.models.task import Task
from app.domain.schemas.task import TaskResponse

@pytest.fixture
def engine():
    """Fixture for database engine"""
    os.environ['TESTING'] = '1'
    return init_db()

@pytest.fixture
def client(engine):
    """Fixture for test client"""
    with TestClient(app) as client:
        yield client
    cleanup_db(engine)

@pytest.mark.integration
class TestTaskIntegration:

    def test_create_task_with_invalid_user(self, client, engine):
        """Test for creating a task with non-existent user"""
        task_data = {
            "user_id": 9999,  # ID no existente
            "type": TaskType.WORK.value,
            "task": "Team meeting",
            "priority": TaskPriority.HIGH.value,
            "status": TaskStatus.PENDING.value,
            "progress": 0
        }
        
        response = client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_create_task(self, client, engine, session: Session):
        """Test for creating a task"""
        # Create user
        user_data = {
            "name": "Test User",
            "surname": "Test",
            "email": "test@example.com",
            "password": "password",
            "role": Role.USER.value
        }
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 201
        user = response.json()

        # Create task list
        list_data = {
            "name": "Test List",
            "description": "Test description",
            "user_id": user["id"]
        }
        response = client.post("/api/v1/tasks_list/", json=list_data)
        assert response.status_code == 201
        task_list = response.json()

        # Create task
        task_data = {
            "user_id": user["id"],
            "type": TaskType.WORK.value,
            "task": "meeting",
            "description": "Meeting with team",
            "priority": TaskPriority.HIGH.value,
            "status": TaskStatus.PENDING.value,
            "progress": 0
        }
        
        response = client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == 201
        
        # Verify response
        task_response = response.json()
        assert task_response["user_id"] == user["id"]
       
        
        # Verify in the database
        task_in_db = session.get(Task, task_response["id"])
        assert task_in_db is not None
        assert task_in_db.task == "meeting"
        assert task_in_db.user_id == user["id"]
        
    
    
       