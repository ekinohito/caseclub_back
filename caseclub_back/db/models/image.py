from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from .attachment import Attachment
if TYPE_CHECKING:
    from .post import Post

class BaseImage(SQLModel):
    data: bytes

class Image(BaseImage, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    posts: List["Post"] = Relationship(back_populates="images", link_model=Attachment)