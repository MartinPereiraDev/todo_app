from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum
from typing import Optional
from app.models.user import User

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
    IN_PROGRESS  =      "in_progress"
    FINISH       =      "finish"

class TaskCreate(SQLModel):
    task:              str
    description:       Optional[str]    = None
    priority:          TaskPriority     = TaskPriority.MEDIUM
    status:            TaskStatus       = TaskStatus.START
    progress:          int              = 0
    user_id:           int

class Task(SQLModel, table=True):
    id:         Optional[int]        = Field(default=None, primary_key=True)
    user_id:    int                  = Field(foreign_key="user.id")
    type:       TaskType             = TaskType.WORK
    task:       str                  = Field(max_length=255)
    priority:   TaskPriority         = TaskPriority.MEDIUM
    status:     TaskStatus           = TaskStatus.START
    progress:   int                  = Field(default=0, ge=0, le=100)  # 0-100
    created_at: datetime             = Field(default_factory=datetime.now)
    updated_at: datetime             = Field(default_factory=datetime.now)
    
    # User relationship
    user: 'User' = Relationship(back_populates="tasks")
