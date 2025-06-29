from fastapi import FastAPI
from app.api.routers import tasks, users, tasks_list
from app.infrastructure.database import init_db, cleanup_db
import os

# Initialize the application
app = FastAPI(
    title="Todo App API",
    description="API para gestión de tareas y listas de tareas",
    version="1.0.0",
    contact={
        "name": "Martin Pereira",
        "email": "martinpereiradeveloper@gmail.com"
    }
)

# Configure routes with static prefixes
app.include_router(tasks.router,        prefix="/api/v1/tasks")
app.include_router(tasks_list.router,   prefix="/api/v1/tasks_list")
app.include_router(users.router,        prefix="/api/v1/users")

async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI"""
    async def startup():
        # Check if we are in test mode
        if os.getenv('TESTING') == '1':
            # Configure SQLite in memory for tests
            from sqlalchemy import create_engine
            from sqlmodel import SQLModel
            
            test_db_url = "sqlite:///:memory:"
            engine = create_engine(test_db_url)
            
            # Create tables
            SQLModel.metadata.create_all(engine)
            
            # Configure the database URL
            os.environ["DATABASE_URL"] = test_db_url
            
            # Initialize database for tests
            init_db()
        else:
            # Initialize the database normally
            init_db()

@app.on_event("shutdown")
async def shutdown():
    cleanup_db()