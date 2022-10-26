from typing import Optional
from sqlmodel import Field, SQLModel

class UserLikesPost(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="user.id")
    post_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="post.id")