import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import config
from app.infrastructure.database import get_session, init_db, get_engine, cleanup_db
from sqlmodel import Session, SQLModel
import os

# Global configuration for all tests
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Configure test environment"""
    # Save the original value of TESTING
    original_testing = os.getenv('TESTING')
    
    try:
        # Configure testing environment
        os.environ["TESTING"] = "1"
        config.TESTING = True
        
        # Initialize the database
        engine = init_db()
        
        yield
        
    finally:
        # Restore the original value of TESTING
        if original_testing is None:
            os.environ.pop('TESTING', None)
        else:
            os.environ['TESTING'] = original_testing
        
        # Clean up after all tests
        cleanup_db(engine)

@pytest.fixture
def client():
    """Test client for the application"""
    # Ensure that the testing environment is configured
    os.environ["TESTING"] = "1"
    config.TESTING = True
    return TestClient(app)

@pytest.fixture
def session():
    """Database session for tests"""
    # Get the correct engine
    engine = get_engine()
    
    # Create a new session
    with Session(engine) as session:
        try:
            # Create tables if they don't exist
            from app.models import User, TaskList, Task
            SQLModel.metadata.create_all(engine)
            
            # Clean up existing data
            # Order tables by dependencies (User first)
            tables = SQLModel.metadata.sorted_tables
            for table in reversed(tables):
                session.execute(table.delete())
            session.commit()
            
            # Verify that the tables exist using the correct API
            from sqlalchemy import inspect
            inspector = inspect(engine)
            assert inspector.has_table("user")
            assert inspector.has_table("task_list")
            assert inspector.has_table("task")
            
            yield session
            
            # Rollback any uncommitted changes
            session.rollback()
        finally:
            # Ensure tables exist
            SQLModel.metadata.create_all(engine)
            
            # Close the session
            session.close()
            
            # Clean up the database
            cleanup_db(engine)
            
            # Create tables again for the next test
            SQLModel.metadata.create_all(engine)

@pytest.fixture
def test_data(session: Session):
    """Create test data"""
    from app.models.user import User
    from app.models.task_list import TaskList
    
    # Create user
    test_user = User(
        name="Test", 
        surname="User", 
        email="test@example.com", 
        password="password"
    )
    session.add(test_user)
    
    # Ensure changes are saved
    session.flush()
    
    # Create task list
    test_list = TaskList(
        name="Test List", 
        user_id=test_user.id
    )
    session.add(test_list)
    
    # Save all changes
    session.commit()
    
    # Refresh entities
    session.refresh(test_user)
    session.refresh(test_list)
    
    return {
        "user": test_user,
        "list": test_list
    }