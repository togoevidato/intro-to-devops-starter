import os
import uuid
import httpx


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


def unique_name(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def test_health_endpoint():
    response = httpx.get(f"{BASE_URL}/health", timeout=5)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_crud_lifecycle():
    fruit_name = unique_name("Dragonfruit")

    create_response = httpx.post(
        f"{BASE_URL}/fruits",
        json={
            "name": fruit_name,
            "price": 5.5,
            "in_season": True
        },
        timeout=5
    )

    assert create_response.status_code == 201

    created_fruit = create_response.json()
    fruit_id = created_fruit["id"]

    get_response = httpx.get(f"{BASE_URL}/fruits/{fruit_id}", timeout=5)

    assert get_response.status_code == 200
    assert get_response.json()["name"] == fruit_name

    update_response = httpx.put(
        f"{BASE_URL}/fruits/{fruit_id}",
        json={
            "price": 4.25
        },
        timeout=5
    )

    assert update_response.status_code == 200
    assert update_response.json()["price"] == 4.25

    delete_response = httpx.delete(f"{BASE_URL}/fruits/{fruit_id}", timeout=5)

    assert delete_response.status_code == 204

    get_deleted_response = httpx.get(f"{BASE_URL}/fruits/{fruit_id}", timeout=5)

    assert get_deleted_response.status_code == 404


def test_cheapest_consistency():
    httpx.post(
        f"{BASE_URL}/fruits",
        json={
            "name": unique_name("CheapFruit"),
            "price": 0.5,
            "in_season": True
        },
        timeout=5
    )

    fruits_response = httpx.get(f"{BASE_URL}/fruits", timeout=5)
    cheapest_response = httpx.get(f"{BASE_URL}/fruits/cheapest", timeout=5)

    assert fruits_response.status_code == 200
    assert cheapest_response.status_code == 200

    fruits = fruits_response.json()
    cheapest = cheapest_response.json()

    minimum_price = min(fruit["price"] for fruit in fruits)

    assert cheapest["price"] == minimum_price


def test_created_fruit_appears_in_fruit_list():
    fruit_name = unique_name("Mango")

    create_response = httpx.post(
        f"{BASE_URL}/fruits",
        json={
            "name": fruit_name,
            "price": 3.75,
            "in_season": False
        },
        timeout=5
    )

    assert create_response.status_code == 201

    list_response = httpx.get(f"{BASE_URL}/fruits", timeout=5)

    assert list_response.status_code == 200

    fruits = list_response.json()

    assert any(fruit["name"] == fruit_name for fruit in fruits)


def test_post_empty_body_returns_error():
    response = httpx.post(f"{BASE_URL}/fruits", json={}, timeout=5)

    assert response.status_code == 422