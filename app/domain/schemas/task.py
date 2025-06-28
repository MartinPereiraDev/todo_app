from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.domain.schemas.user import UserResponse
from pydantic.config import ConfigDict

class TaskCreate(BaseModel):
    task:       str
    type:       str
    priority:   str
    status:     str
    progress:   int
    user_id:    int
    task:       str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class TaskResponse(BaseModel):
    id:         int
    user: UserResponse
    type:       str
    task:       str
    priority:   str
    status:     str
    progress:   int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


