from typing import List

from .auth import get_password_hash, get_current_user
from ..db.models import UserCreate, UserRead, User
from ..db.database import engine
from fastapi import APIRouter, HTTPException, Depends 
from sqlmodel import Session, select
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/", response_model=UserRead, responses={404: {"description": "User exists"}})
async def create_user(user: UserCreate):
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.email == user.email)).first()
        if existing_user is not None:
            raise HTTPException(400, "User with this email already exists")
        hashed_password = get_password_hash(user.password)
        user: User = User.from_orm(user, {"hashed_password": hashed_password})
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@router.get("/", response_model=List[UserRead])
async def get_users(offset: int=0, limit: int=20):
    with Session(engine) as session:
        return session.exec(select(User).offset(offset).limit(limit)).all()

@router.get("/secret")
async def secret(user: User = Depends(get_current_user)):
    return "secret " + user.email

@router.get("/{id}", response_model=UserRead, responses={404: {"description": "Not found"}})
async def get_users(id: int):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == id)).first()
        if user is None:
            raise HTTPException(404, "User not found")
        return user

@router.delete("/{id}", response_model=UserRead, responses={404: {"description": "Not found"}})
async def delete_user(id: int):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == id)).first()
        if user is None:
            raise HTTPException(404, "User not found")
        session.delete(user)
        session.commit()
        return user
