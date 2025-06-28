import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.infrastructure.database import init_db, get_session

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    """Initialize database before each test"""
    init_db()
    yield
    # Cleanup after test

def test_create_todo_list():
    """Test creating a new todo list"""
    response = client.post("/lists/", json={"title": "Work Tasks"})
    assert response.status_code == 201
    assert response.json()["title"] == "Work Tasks"
    assert "id" in response.json()

def test_get_tasks_with_completion():
    """Test getting tasks with completion percentage"""
    # Create list and tasks first
    list_res = client.post("/lists/", json={"title": "Test List"})
    list_id = list_res.json()["id"]
    
    # Create tasks
    for i in range(3):
        client.post(f"/lists/{list_id}/tasks", json={"title": f"Task {i}"})
    
    # Test without filters
    response = client.get(f"/lists/{list_id}/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["completion_percentage"] is None
    
    # Test with filter
    response = client.get(f"/lists/{list_id}/tasks?status=done")
    assert response.status_code == 200
    assert len(response.json()) == 0
    assert response.json()[0]["completion_percentage"] == 0.0