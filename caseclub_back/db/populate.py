from sqlmodel import Session
from .database import engine
from .models import Post, UserCreate
from ..utils.password_hash import register_user

def populate():
    with Session(engine) as session:
        session.add(Post(text="first post"))
        session.add(Post(text="second post"))
        session.add(Post(text="third post"))
        session.add(register_user(UserCreate(email="user1@gmail.com", name="User #1", password="weak_password")))
        session.commit()