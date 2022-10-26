from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from .user_attends_event import UserAttendsEvent
if TYPE_CHECKING:
    from .user import User

class BaseEvent(SQLModel):
    title: str = ''
    text: str = ''
    icon: str = ''
    start_date: datetime
    end_date: datetime

class Event(BaseEvent, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    users: List["User"] = Relationship(back_populates="events", link_model=UserAttendsEvent)

class EventCreate(BaseEvent):
    pass

class EventRead(BaseEvent):
    id: int