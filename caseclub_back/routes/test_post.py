from fastapi.testclient import TestClient
from sqlmodel import Session

from ..db.models.post import Post

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
    response = client.get(
        f"/post/{id}/",
    )
    data = response.json()
    assert response.status_code == 200
    assert data["text"] == "First post"
    assert data["id"] == id