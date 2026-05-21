import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api import app
from app.database import Base, get_db
from app.models import FruitEntity
from app.store import build_fruit_response, seed_fruits


TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_test_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    try:
        seed_fruits(db)
    finally:
        db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield

    app.dependency_overrides.clear()


client = TestClient(app)


def clear_fruits():
    db = TestingSessionLocal()

    try:
        db.query(FruitEntity).delete()
        db.commit()
    finally:
        db.close()


def test_build_fruit_response_returns_expected_structure():
    fruit = build_fruit_response(
        fruit_id=10,
        name="Kiwi",
        price=3.25,
        in_season=True
    )

    assert fruit == {
        "id": 10,
        "name": "Kiwi",
        "price": 3.25,
        "in_season": True
    }


def test_list_fruits_returns_fixture_data():
    response = client.get("/fruits")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Apple", "price": 1.5, "in_season": True},
        {"id": 2, "name": "Banana", "price": 0.9, "in_season": True},
        {"id": 3, "name": "Orange", "price": 2.0, "in_season": False}
    ]


def test_get_cheapest_fruit_returns_cheapest_fixture_fruit():
    response = client.get("/fruits/cheapest")

    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "name": "Banana",
        "price": 0.9,
        "in_season": True
    }


def test_filter_fruits_in_season_true():
    response = client.get("/fruits?in_season=true")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Apple", "price": 1.5, "in_season": True},
        {"id": 2, "name": "Banana", "price": 0.9, "in_season": True}
    ]


def test_filter_fruits_in_season_false():
    response = client.get("/fruits?in_season=false")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 3, "name": "Orange", "price": 2.0, "in_season": False}
    ]


def test_get_unknown_fruit_returns_404():
    response = client.get("/fruits/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Fruit not found"}


def test_post_invalid_fruit_returns_422():
    response = client.post("/fruits", json={
        "name": "Invalid Fruit",
        "price": "not-a-number"
    })

    assert response.status_code == 422


def test_put_unknown_fruit_returns_404():
    response = client.put("/fruits/999", json={
        "price": 4.5
    })

    assert response.status_code == 404
    assert response.json() == {"detail": "Fruit not found"}


def test_delete_unknown_fruit_returns_404():
    response = client.delete("/fruits/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Fruit not found"}


def test_get_cheapest_when_no_fruits_returns_404():
    clear_fruits()

    response = client.get("/fruits/cheapest")

    assert response.status_code == 404
    assert response.json() == {"detail": "No fruits found"}