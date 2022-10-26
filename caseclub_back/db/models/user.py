from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from .user_likes_post import UserLikesPost
from .user_attends_event import UserAttendsEvent
if TYPE_CHECKING:
    from .post import Post
    from .event import Event
    from .image import Image

class BaseUser(SQLModel):
    roles: Optional[str] = None
    email: str = Field(index=True, unique=True)
    name: str
    image_id: Optional[int] = Field(default=None, foreign_key="image.id")

class User(BaseUser, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    liked_posts: List["Post"] = Relationship(back_populates="users", link_model=UserLikesPost)
    events: List["Event"] = Relationship(back_populates="users", link_model=UserAttendsEvent)
    image: "Image" = Relationship()

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