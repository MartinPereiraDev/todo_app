from pydantic import BaseModel, EmailStr
from enum import Enum

class Role(str, Enum):
    USER     = "user"
    ADMIN    = "admin"
    MANAGER  = "manager"

class UserCreate(BaseModel):
    name:       str
    surname:    str
    email:      EmailStr
    password:   str
    role:       Role = Role.USER

class UserResponse(BaseModel):
    id:         int
    name:       str
    surname:    str
    email:      str
    role:       Role

class UserLogin(BaseModel):
    email:      EmailStr
    password:   str