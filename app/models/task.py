from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum
from typing import Optional
from app.models.user import User
from app.models.task_list import TaskList

class TaskType(str, Enum):
    WORK     =      "work"
    PERSONAL =      "personal"
    OTHER    =      "other"

class TaskPriority(str, Enum):
    LOW      =      "low"
    MEDIUM   =      "medium"
    HIGH     =      "high"

class TaskStatus(str, Enum):
    START        =      "start"
    PENDING      =      "pending"
    IN_PROGRESS  =      "in_progress"
    DONE         =      "done"

class Task(SQLModel, table=True):
    id:         Optional[int]        = Field(default=None, primary_key=True)
    user_id:    int                  = Field(foreign_key="user.id")
    list_id:    Optional[int]        = Field(foreign_key="task_list.id")
    type:       TaskType             = Field(default=TaskType.WORK)
    task:       str                  = Field(max_length=255)
    description: Optional[str]       = Field(default=None, max_length=255)
    priority:   TaskPriority         = Field(default=TaskPriority.MEDIUM)
    status:     str                  = Field(default="START")  
    progress:   int                  = Field(default=0, ge=0, le=100)  # 0-100
    created_at: datetime             = Field(default_factory=datetime.utcnow)
    updated_at: datetime             = Field(default_factory=datetime.utcnow)
    
    # Relaciones
    user: User = Relationship(back_populates="tasks", sa_relationship_kwargs={"primaryjoin": "User.id == Task.user_id"})
    task_list: 'TaskList' = Relationship(back_populates="tasks", sa_relationship_kwargs={"primaryjoin": "Task.list_id == TaskList.id"})
