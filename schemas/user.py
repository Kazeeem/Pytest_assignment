from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: str
    name: str
    username: str
    password: str
    email: str
    age: Optional[int] = None
    phone: Optional[str] = None

class UserCreate(BaseModel):
    name: str
    email: str
    username: str
    password: str
    age: Optional['int'] = None
    phone: Optional['str'] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None

class Users(BaseModel):
    users: list[User]

class Response(BaseModel):
    message: Optional[str] = None
    has_error: bool = False
    error_message: Optional[str] = None
    data: Optional[User | Users] = None

class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_new_password: str

class UserLogin(BaseModel):
    username: str
    password: str
