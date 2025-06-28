from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import config
from app.models import User, TaskList, Task

DATABASE_URL = config.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # SQLModel.metadata.create_all(engine)  # This line is commented out because SQLModel is no longer imported
    pass

def get_session():
    with SessionLocal() as session:
        yield session