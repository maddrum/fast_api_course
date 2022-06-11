from typing import Optional

from pydantic import BaseModel, Field


class TodoItem(BaseModel):
    title: str = Field(min_length=1, title='Title of book')
    description: str = Field(min_length=1, title='Title of book')
    priority: int = Field(le=100, ge=0)
    complete: bool = Field(default=False)

    class Config:
        schema_extra = {
            'example':
                {
                    'title': 'Feed the cat',
                    'description': 'The cat is hungry too much! Cat is always hungry!',
                    'priority': 5,
                    'complete': False,
                }

        }


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str


class LoginUser(BaseModel):
    username: str
    password: str
