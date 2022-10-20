from datetime import datetime
from typing import List
from random import choice
from sqlmodel import Session
from os.path import join
from pathlib import Path
from .database import engine
from .models import Event, Image, Post, UserCreate
from ..utils.password_hash import register_user

def get_mocks_generator():
    mocks: List[bytes] = []
    mocks_path = Path("caseclub_back", "db", "mocks")
    for file in mocks_path.glob("*.jpg"):
        with open(file, "rb") as mock:
            mocks.append(mock.read())
    while True:
        yield Image(data=choice(mocks))

mock_generator = get_mocks_generator()

def populate_users(session: Session):
    admin = register_user(UserCreate(email="admin@localhost", name="Admin", password="root", roles="admin"))
    admin.image = mock_generator.__next__()
    users = [
        admin,
        register_user(UserCreate(email="user1@gmail.com", name="User #1", password="weak_password")),
        register_user(UserCreate(email="user2@yandex.ru", name="User #2", password="strong_password")),
        register_user(UserCreate(email="user3@mail.ru", name="User #3", password="pwd")),
    ]
    session.add_all(users)
    session.commit()

def populate_posts(session: Session):
    posts = [
        Post(text="Первый пост", images=[mock_generator.__next__(), mock_generator.__next__()]),
        Post(text="Второй пост"),
        Post(text="Третий пост", images=[mock_generator.__next__()]),
    ]
    session.add_all(posts)
    session.commit()

def populate_events(session: Session):
    events = [
        Event(title="Кейс-чемпионат", text='Lorem ipsum', icon='💼', start_date=datetime(2022, 10, 17, 9), end_date=datetime(2022, 10, 24, 0)),
        Event(title="Занятие", text='Lorem ipsum', icon='👩‍🎓', start_date=datetime(2022, 10, 5, 17), end_date=datetime(2022, 10, 5, 19)),
        Event(title="Занятие", text='Lorem ipsum', icon='👩‍🎓', start_date=datetime(2022, 10, 12, 17), end_date=datetime(2022, 10, 12, 19)),
        Event(title="Занятие", text='Lorem ipsum', icon='👩‍🎓', start_date=datetime(2022, 10, 19, 17), end_date=datetime(2022, 10, 19, 19)),
        Event(title="Занятие", text='Lorem ipsum', icon='👩‍🎓', start_date=datetime(2022, 10, 26, 17), end_date=datetime(2022, 10, 26, 19)),
        Event(title="Награждение победителей", text='Lorem ipsum', icon='🥇', start_date=datetime(2022, 10, 26, 19), end_date=datetime(2022, 10, 26, 20)),
    ]
    session.add_all(events)
    session.commit()

def populate():
    with Session(engine) as session:
        populate_users(session)
        populate_posts(session)
        populate_events(session)
