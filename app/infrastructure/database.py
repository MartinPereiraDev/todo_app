from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings
from app.models.user import User

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session