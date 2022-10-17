from sqlmodel import Session
from os.path import join
from pathlib import Path
from .database import engine
from .models import Image, Post, UserCreate
from ..utils.password_hash import register_user

def populate():
    with Session(engine) as session:
        mocks = []
        mocks_path = Path("caseclub_back", "db", "mocks")
        for file in mocks_path.glob("*.jpg"):
            with open(file, "rb") as file:
                mock = Image(data=file.read())
                mocks.append(mock)

        session.add(Post(text="first post", images=mocks[:2]))
        session.add(Post(text="second post"))
        session.add(Post(text="third post"))
        session.add(register_user(UserCreate(email="user1@gmail.com", name="User #1", password="weak_password")))
        session.add(register_user(UserCreate(email="admin@localhost", name="Admin", password="root")))
        session.commit()