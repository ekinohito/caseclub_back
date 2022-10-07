from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class BasePost(SQLModel):
    text: str

class Post(BasePost, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    likes: Optional[int] = 0

class PostCreate(BasePost):
    pass

class PostRead(BasePost):
    id: int
    likes: int


class BaseUser(SQLModel):
    email: str = Field(index=True)
    name: str

class User(BaseUser, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(BaseUser):
    password: str

class UserRead(BaseUser):
    id: int

class UserLogin(SQLModel):
    email: str
    password: str

