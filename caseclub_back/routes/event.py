from datetime import datetime
from typing import List
from ..db.models.event import Event, EventRead
from .auth import require_current_user, get_current_user
from ..db.models.user import User
from ..db.database import get_session
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session

router = APIRouter(prefix="/event", tags=["event"])

async def get_event(id: int, session: Session = Depends(get_session)):
    event = session.exec(select(Event).where(Event.id == id)).first()
    if event is None:
        raise HTTPException(404, "Event not found")
    return event

@router.get("/", response_model=List[EventRead])
async def get_events(since:datetime, until:datetime, session:Session=Depends(get_session), user: User = Depends(get_current_user)):
    events = session.exec(select(Event).where(Event.start_date < until, Event.end_date >= since).order_by(Event.start_date)).all()
    return [EventRead.from_orm(event, {'is_attended': user in event.users}) for event in events]

id_router = APIRouter(prefix="/{id}")

@id_router.get("/", response_model=EventRead, responses={404: {"description": "Not found"}})
async def get_event(event: Event = Depends(get_event)):
    return event

@id_router.post("/attend")
async def attend_event(event: Event = Depends(get_event), user: User = Depends(require_current_user), session: Session = Depends(get_session)):
    event.users.append(user)
    session.add(event)
    session.commit()
    return "ok"

@id_router.post("/stop_attend")
async def attend_event(event: Event = Depends(get_event), user: User = Depends(require_current_user), session: Session = Depends(get_session)):
    event.users.remove(user)
    session.add(event)
    session.commit()
    return "ok"

router.include_router(id_router)