from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

class UserLikesPost(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="user.id")
    post_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="post.id")

class BasePost(SQLModel):
    text: str

class Post(BasePost, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    likes: Optional[int] = 0
    users: List["User"] = Relationship(back_populates="liked_posts", link_model=UserLikesPost)

class PostCreate(BasePost):
    pass

class PostRead(BasePost):
    id: int
    likes: int

class PostEdit(SQLModel):
    text: Optional[str]


class BaseUser(SQLModel):
    email: str = Field(index=True, unique=True)
    name: str
    picture: Optional[str] = None

class User(BaseUser, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    liked_posts: List["Post"] = Relationship(back_populates="users", link_model=UserLikesPost)

class UserCreate(BaseUser):
    password: str

class UserRead(BaseUser):
    id: int

class UserLogin(SQLModel):
    email: str
    password: str

class UserEdit(SQLModel):
    email: Optional[str]
    name: Optional[str]
    password: Optional[str]
    picture: Optional[str]

