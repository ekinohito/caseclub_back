import os
from sqlmodel import SQLModel, create_engine, Session
from .models import *

postgres_url=os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@localhost:5433/caseclub'

engine = create_engine(postgres_url)


def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
