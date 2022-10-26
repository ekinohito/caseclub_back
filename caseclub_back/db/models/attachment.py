from typing import Optional
from sqlmodel import Field, SQLModel


class Attachment(SQLModel, table=True):
    post_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="post.id")
    image_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="image.id")
