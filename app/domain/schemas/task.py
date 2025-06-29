from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from app.domain.schemas.user import UserResponse, UserResponseTaskList
from pydantic.config import ConfigDict
from app.models.task import TaskType, TaskPriority, TaskStatus

# Schema for updating task status and priority
class TaskUpdate(BaseModel):
    status      : Optional[TaskStatus] = None
    priority    : Optional[TaskPriority] = None
    progress    : Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

# Schema for creating a new task
class TaskCreate(BaseModel):
    user_id     :   int
    list_id     :   Optional[int] = None  
    task        :   str
    type        :   TaskType
    description :   Optional[str] = None
    priority    :   TaskPriority
    status      :   TaskStatus
    progress    :   Optional[int] = 0
    created_at  :   Optional[datetime] = None
    updated_at  :   Optional[datetime] = None

    

class TaskResponse(BaseModel):
    id          :   int
    user        : UserResponseTaskList
    type        :   TaskType
    task        :   str
    description :   Optional[str] = None
    priority    :   TaskPriority
    status      :   TaskStatus
    progress    :   int
    created_at  :   Optional[datetime] = None
    updated_at  :   Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


