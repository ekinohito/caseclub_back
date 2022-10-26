from typing import Optional
from sqlmodel import Field, SQLModel

class UserAttendsEvent(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="user.id")
    event_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="event.id")
