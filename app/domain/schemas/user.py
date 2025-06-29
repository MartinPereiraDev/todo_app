from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class Role(str, Enum):
    USER     = "user"
    ADMIN    = "admin"
    MANAGER  = "manager"

class UserCreate(BaseModel):
    name        :   str
    surname     :   str
    email       :   EmailStr
    password    :   str
    role        :   Role = Role.USER

class UserResponse(BaseModel):
    id          :   int
    name        :   str
    surname     :   str
    email       :   str
    role        :   Role

class UserResponseTaskList(BaseModel):
    id          :   int
    name        :   str
    surname     :   str
    email       :   str

class UserUpdate(BaseModel):
    name        :   Optional[str] = None
    surname     :   Optional[str] = None
    email       :   Optional[EmailStr] = None
    role        :   Optional[Role] = None    

class UserLogin(BaseModel):
    email       :   EmailStr
    password    :   str