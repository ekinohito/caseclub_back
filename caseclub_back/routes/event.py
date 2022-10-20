from datetime import datetime
from typing import List, Optional
from ..db.models import Attachment, Event, EventRead, Image, PostCreate, PostEdit, PostRead, Post, User, UserLikesPost
from ..db.database import get_session
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session, or_, and_

router = APIRouter(prefix="/event", tags=["event"])

async def get_event(id: int, session: Session = Depends(get_session)):
    event = session.exec(select(Event).where(Event.id == id)).first()
    if event is None:
        raise HTTPException(404, "Event not found")
    return event

@router.get("/", response_model=List[EventRead])
async def get_events(since:datetime, until:datetime, session:Session=Depends(get_session)):
    return session.exec(select(Event).where(Event.start_date < until, Event.end_date >= since).order_by(Event.start_date)).all()

id_router = APIRouter(prefix="/{id}")

@id_router.get("/", response_model=EventRead, responses={404: {"description": "Not found"}})
async def get_event(event: Event = Depends(get_event)):
    return event

router.include_router(id_router)