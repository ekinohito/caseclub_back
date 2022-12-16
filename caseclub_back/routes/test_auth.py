import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from jose import jwt

from ..db.models.user import User
from ..routes.auth import SECRET_KEY
from ..utils.password_hash import get_password_hash

@pytest.fixture(autouse=True)
def add_user(session: Session):
    hashed_password = get_password_hash("secret")
    user: User = User(
        name="user",
        email="user@example.com",
        hashed_password=hashed_password
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    print(user)

def test_get_token(client: TestClient):
    
    response = client.post(
        "/auth/token",
        files={
            "username": (None, "user@example.com"),
            "password": (None, "secret"),
        }
    )
    data = response.json()

    assert response.status_code == 200
    assert data["token_type"] == "bearer"
    token = jwt.decode(data["access_token"], SECRET_KEY)
    assert token["email"] == "user@example.com"

def test_wrong_password(client: TestClient):
    response = client.post(
        "/auth/token",
        files={
            "username": (None, "user@example.com"),
            "password": (None, "wrong"),
        }
    )

    assert response.status_code == 401