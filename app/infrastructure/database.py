from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from app.core.config import config
from app.models import User, TaskList, Task
import os

# Initialize engine and session based on environment
def get_engine():
    """Get the appropriate engine based on environment"""
    if os.getenv('TESTING') == '1':
        # Use SQLite in memory for tests
        engine = create_engine("sqlite:///:memory:", echo=True)
        return engine
    
    # Use MySQL for production
    return create_engine(config.DATABASE_URL, echo=True)

def init_db():
    """Initialize database tables"""
    # Get the appropriate engine
    engine = get_engine()
    
    # Create tables
    SQLModel.metadata.create_all(engine)
    return engine

def get_session():
    """Get a database session"""
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        # Create tables if it's a new SQLite in-memory session
        if os.getenv('TESTING') == '1':
            SQLModel.metadata.create_all(engine)
        
        yield session
    finally:
        session.close()

def cleanup_db(engine):
    """Cleanup database connections"""
    # For SQLite in tests, drop all tables
    if os.getenv('TESTING') == '1':
        SQLModel.metadata.drop_all(engine)
        engine.dispose()