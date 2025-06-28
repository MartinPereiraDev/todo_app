from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from app.models.user import User

class TaskList(SQLModel, table=True):
    __tablename__ = 'task_list'
    id:             Optional[int]        = Field(default=None, primary_key=True)
    user_id:        int                  = Field(foreign_key="user.id")
    name:           str                  = Field(max_length=255)
    description:    Optional[str]        = Field(default=None, max_length=255)
    created_at:     datetime             = Field(default_factory=datetime.now)
    updated_at:     datetime             = Field(default_factory=datetime.now)
    
    # Relaciones
    user: User = Relationship(back_populates="lists", sa_relationship_kwargs={"primaryjoin": "User.id == TaskList.user_id"})
    tasks: List['Task'] = Relationship(back_populates="task_list", sa_relationship_kwargs={"primaryjoin": "Task.list_id == TaskList.id"})
