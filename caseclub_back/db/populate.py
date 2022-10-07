from sqlmodel import Session
from .database import engine
from .models import Post

def populate():
    with Session(engine) as session:
        session.add(Post(text="first post"))
        session.add(Post(text="second post"))
        session.add(Post(text="third post"))
        session.commit()