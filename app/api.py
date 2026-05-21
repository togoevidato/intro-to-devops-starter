import asyncio
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, Response
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from app.database import Base, SessionLocal, engine, get_db
from app.models import Fruit, FruitCreate, FruitUpdate
from app.store import (
    create_fruit,
    delete_fruit,
    get_cheapest_fruit,
    get_fruit,
    list_fruits,
    seed_fruits,
    update_fruit
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    max_attempts = 30
    delay_seconds = 2

    for attempt in range(1, max_attempts + 1):
        try:
            Base.metadata.create_all(bind=engine)

            db = SessionLocal()

            try:
                seed_fruits(db)
            finally:
                db.close()

            break
        except OperationalError:
            if attempt == max_attempts:
                raise

            await asyncio.sleep(delay_seconds)

    yield


app = FastAPI(title="FruitAPI", lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/fruits", response_model=list[Fruit])
def get_fruits(
    in_season: bool | None = Query(default=None),
    db: Session = Depends(get_db)
):
    return list_fruits(db, in_season=in_season)


@app.post("/fruits", response_model=Fruit, status_code=201)
def post_fruit(
    fruit: FruitCreate,
    db: Session = Depends(get_db)
):
    return create_fruit(db, fruit)


@app.get("/fruits/cheapest", response_model=Fruit)
def get_cheapest(db: Session = Depends(get_db)):
    fruit = get_cheapest_fruit(db)

    if fruit is None:
        raise HTTPException(status_code=404, detail="No fruits found")

    return fruit


@app.get("/fruits/{fruit_id}", response_model=Fruit)
def get_fruit_by_id(
    fruit_id: int,
    db: Session = Depends(get_db)
):
    fruit = get_fruit(db, fruit_id)

    if fruit is None:
        raise HTTPException(status_code=404, detail="Fruit not found")

    return fruit


@app.put("/fruits/{fruit_id}", response_model=Fruit)
def put_fruit(
    fruit_id: int,
    fruit: FruitUpdate,
    db: Session = Depends(get_db)
):
    updated_fruit = update_fruit(db, fruit_id, fruit)

    if updated_fruit is None:
        raise HTTPException(status_code=404, detail="Fruit not found")

    return updated_fruit


@app.delete("/fruits/{fruit_id}", status_code=204)
def remove_fruit(
    fruit_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_fruit(db, fruit_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Fruit not found")

    return Response(status_code=204)