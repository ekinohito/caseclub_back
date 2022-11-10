from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from .user_likes_post import UserLikesPost
from .attachment import Attachment
if TYPE_CHECKING:
    from .user import User
    from .image import Image

class BasePost(SQLModel):
    text: str

class Post(BasePost, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    likes: Optional[int] = 0
    users: List["User"] = Relationship(back_populates="liked_posts", link_model=UserLikesPost)
    images: List["Image"] = Relationship(back_populates="posts", link_model=Attachment)

class PostCreate(BasePost):
    images: List[int]

class PostRead(BasePost):
    id: int
    likes: int
    is_liked: Optional[bool]
    images: List[int]
    created_at: datetime

class PostEdit(SQLModel):
    text: Optional[str]