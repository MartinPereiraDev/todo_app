from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum
from typing import Optional, List

class Role(str, Enum):
    USER     =      "user"
    ADMIN    =      "admin"
    MANAGER  =      "manager"

class User(SQLModel, table=True):
    id:         Optional[int]        = Field(default=None, primary_key=True)
    name:       str                  = Field(max_length=50)
    surname:    str                  = Field(max_length=50)
    email:      str                  = Field(max_length=100, unique=True, index=True)
    password:   str                  = Field(max_length=255)
    role:       Role                 = Field(default=Role.USER)
    
    # Relaciones
    tasks: List['Task'] = Relationship(back_populates="user")
    lists: List['TaskList'] = Relationship(back_populates="user")
    lists: List['TaskList'] = Relationship(back_populates="user")
