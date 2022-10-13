from datetime import datetime
import enum
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

class UserLikesPost(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="user.id")
    post_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="post.id")

class Attachment(SQLModel, table=True):
    post_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="post.id")
    image_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="image.id")

class BasePost(SQLModel):
    text: str

class Post(BasePost, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    likes: Optional[int] = 0
    users: List["User"] = Relationship(back_populates="liked_posts", link_model=UserLikesPost)
    images: List["Image"] = Relationship(back_populates="posts", link_model=Attachment)

class PostCreate(BasePost):
    pass

class PostRead(BasePost):
    id: int
    likes: int
    is_liked: Optional[bool]
    images: List[int]

class PostEdit(SQLModel):
    text: Optional[str]


class BaseUser(SQLModel):
    email: str = Field(index=True, unique=True)
    name: str
    image_id: Optional[int] = Field(default=None, foreign_key="image.id")

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



class BaseImage(SQLModel):
    data: bytes

class Image(BaseImage, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    posts: List[Post] = Relationship(back_populates="images", link_model=Attachment)
