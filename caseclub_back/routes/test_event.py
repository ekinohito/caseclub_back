from fastapi.testclient import TestClient
from sqlmodel import Session
from datetime import datetime

from ..db.models.event import Event

def test_get_events(session: Session, client: TestClient):
    session.add(Event(
        title="First Event",
        text="Description 1",
        start_date=datetime(2022, 10, 14),
        end_date=datetime(2022, 10, 14),
    ))
    session.add(Event(
        title="Second Event",
        text="Description 2",
        start_date=datetime(2022, 10, 15),
        end_date=datetime(2022, 10, 16),
    ))
    session.add(Event(
        title="Third Event",
        text="Description 3",
        start_date=datetime(2022, 11, 17),
        end_date=datetime(2022, 11, 17),
    ))
    session.commit()
    response = client.get(
        "/event/", params={"since": datetime(2022, 10, 1), "until": datetime(2022, 11, 1)}
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["title"] == "First Event"
    assert data[0]["text"] == "Description 1"
    assert data[1]["title"] == "Second Event"
    assert data[1]["text"] == "Description 2"

def test_get_event(session: Session, client: TestClient):
    event = Event(
        title="First Event",
        text="Description 1",
        start_date=datetime(2022, 10, 14),
        end_date=datetime(2022, 10, 14),
    )
    session.add(event)
    session.commit()
    id = event.id
    response = client.get(
        f"/event/{id}/",
    )
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == id
    assert data["title"] == "First Event"
    assert data["text"] == "Description 1"