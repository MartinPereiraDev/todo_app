from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from app.domain.schemas.user import UserResponse, UserResponseTaskList
from pydantic.config import ConfigDict
from app.models.task import TaskType, TaskPriority, TaskStatus

class TaskCreate(BaseModel):
    user_id:    int
    list_id:    Optional[int] = None  # ID de la lista de tareas
    task:       str
    type:       TaskType
    description: Optional[str] = None
    priority:   TaskPriority
    status:     TaskStatus
    progress:   Optional[int] = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    

class TaskResponse(BaseModel):
    id:         int
    user: UserResponseTaskList
    type:       TaskType
    task:       str
    description:Optional[str] = None
    priority:   TaskPriority
    status:     TaskStatus
    progress:   int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


