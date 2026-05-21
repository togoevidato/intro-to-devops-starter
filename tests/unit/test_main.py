import app.store as store
from fastapi.testclient import TestClient
from app.api import app
from app.store import build_fruit_response


client = TestClient(app)


def reset_store():
    store._fruits = {
        1: {"id": 1, "name": "Apple", "price": 1.5, "in_season": True},
        2: {"id": 2, "name": "Banana", "price": 0.9, "in_season": True},
        3: {"id": 3, "name": "Orange", "price": 2.0, "in_season": False}
    }
    store._next_id = 4


def setup_function():
    reset_store()


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
    store._fruits = {}

    response = client.get("/fruits/cheapest")

    assert response.status_code == 404
    assert response.json() == {"detail": "No fruits found"}