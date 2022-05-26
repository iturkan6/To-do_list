from typing import Union

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: Union[str, None] = None


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    name: str
    surname: Union[str, None] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    tasks: list[Task] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
