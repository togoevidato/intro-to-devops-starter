from threading import Lock
from app.models import FruitCreate, FruitUpdate


_lock = Lock()

_fruits = {
    1: {"id": 1, "name": "Apple", "price": 1.5, "in_season": True},
    2: {"id": 2, "name": "Banana", "price": 0.9, "in_season": True},
    3: {"id": 3, "name": "Orange", "price": 2.0, "in_season": False}
}

_next_id = 4


def build_fruit_response(fruit_id: int, name: str, price: float, in_season: bool) -> dict:
    return {
        "id": fruit_id,
        "name": name,
        "price": price,
        "in_season": in_season
    }


def list_fruits(in_season: bool | None = None) -> list[dict]:
    fruits = list(_fruits.values())

    if in_season is not None:
        fruits = [fruit for fruit in fruits if fruit["in_season"] == in_season]

    return fruits


def get_fruit(fruit_id: int) -> dict | None:
    return _fruits.get(fruit_id)


def create_fruit(data: FruitCreate) -> dict:
    global _next_id

    with _lock:
        fruit = build_fruit_response(
            fruit_id=_next_id,
            name=data.name,
            price=data.price,
            in_season=data.in_season
        )

        _fruits[_next_id] = fruit
        _next_id += 1

        return fruit


def update_fruit(fruit_id: int, data: FruitUpdate) -> dict | None:
    with _lock:
        fruit = _fruits.get(fruit_id)

        if fruit is None:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            fruit[key] = value

        return fruit


def delete_fruit(fruit_id: int) -> bool:
    with _lock:
        if fruit_id not in _fruits:
            return False

        del _fruits[fruit_id]
        return True


def get_cheapest_fruit() -> dict | None:
    if not _fruits:
        return None

    return min(_fruits.values(), key=lambda fruit: fruit["price"])