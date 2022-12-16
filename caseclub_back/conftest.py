import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from .main import app
from .db.models import *
from .db.models.post import Post
from .db.database import get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_post_post(client: TestClient):
    response = client.post(
        "/post/", json={
            "text": "Some post",
            "images": [],
        }
    )
    data = response.json()

    assert response.status_code == 200
    assert data["text"] == "Some post"
    assert data["id"] is not None
    assert data["created_at"] is not None
    assert data["likes"] == 0
    assert len(data["images"]) == 0

def test_get_posts(session: Session, client: TestClient):
    session.add(Post(text="First post"))
    session.add(Post(text="Second post"))
    session.commit()
    response = client.get(
        "/post/",
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["text"] == "Second post"
    assert data[1]["text"] == "First post"

def test_get_post(session: Session, client: TestClient):
    post = Post(text="First post")
    session.add(post)
    session.commit()
    id = post.id
    print(id)
    response = client.get(
        f"/post/{id}/",
    )
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert data["text"] == "First post"
    assert data["id"] == id


