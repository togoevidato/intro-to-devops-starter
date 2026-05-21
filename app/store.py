from sqlalchemy.orm import Session
from app.models import FruitCreate, FruitEntity, FruitUpdate


def build_fruit_response(fruit_id: int, name: str, price: float, in_season: bool) -> dict:
    return {
        "id": fruit_id,
        "name": name,
        "price": price,
        "in_season": in_season
    }


def seed_fruits(db: Session) -> None:
    existing_fruit = db.query(FruitEntity).first()

    if existing_fruit is not None:
        return

    fruits = [
        FruitEntity(name="Apple", price=1.5, in_season=True),
        FruitEntity(name="Banana", price=0.9, in_season=True),
        FruitEntity(name="Orange", price=2.0, in_season=False)
    ]

    db.add_all(fruits)
    db.commit()


def list_fruits(db: Session, in_season: bool | None = None) -> list[FruitEntity]:
    query = db.query(FruitEntity)

    if in_season is not None:
        query = query.filter(FruitEntity.in_season == in_season)

    return query.order_by(FruitEntity.id).all()


def get_fruit(db: Session, fruit_id: int) -> FruitEntity | None:
    return db.query(FruitEntity).filter(FruitEntity.id == fruit_id).first()


def create_fruit(db: Session, data: FruitCreate) -> FruitEntity:
    fruit = FruitEntity(
        name=data.name,
        price=data.price,
        in_season=data.in_season
    )

    db.add(fruit)
    db.commit()
    db.refresh(fruit)

    return fruit


def update_fruit(db: Session, fruit_id: int, data: FruitUpdate) -> FruitEntity | None:
    fruit = get_fruit(db, fruit_id)

    if fruit is None:
        return None

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(fruit, key, value)

    db.commit()
    db.refresh(fruit)

    return fruit


def delete_fruit(db: Session, fruit_id: int) -> bool:
    fruit = get_fruit(db, fruit_id)

    if fruit is None:
        return False

    db.delete(fruit)
    db.commit()

    return True


def get_cheapest_fruit(db: Session) -> FruitEntity | None:
    return db.query(FruitEntity).order_by(FruitEntity.price.asc()).first()