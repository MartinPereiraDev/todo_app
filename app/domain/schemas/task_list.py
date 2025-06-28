from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.domain.schemas.user import UserResponse
from app.domain.schemas.task import TaskResponse
from pydantic.config import ConfigDict

class TaskListCreate(BaseModel):
    name: str
    description: Optional[str] = None
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class TaskListResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    tasks: list[TaskResponse] = []

    model_config = ConfigDict(from_attributes=True)
