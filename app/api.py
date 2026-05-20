from fastapi import FastAPI, HTTPException, Response, Query
from app.models import Fruit, FruitCreate, FruitUpdate
from app.store import (
    list_fruits,
    get_fruit,
    create_fruit,
    update_fruit,
    delete_fruit,
    get_cheapest_fruit
)


app = FastAPI(title="FruitAPI")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/fruits", response_model=list[Fruit])
def get_fruits(in_season: bool | None = Query(default=None)):
    return list_fruits(in_season=in_season)


@app.post("/fruits", response_model=Fruit, status_code=201)
def post_fruit(fruit: FruitCreate):
    return create_fruit(fruit)


@app.get("/fruits/cheapest", response_model=Fruit)
def get_cheapest():
    fruit = get_cheapest_fruit()

    if fruit is None:
        raise HTTPException(status_code=404, detail="No fruits found")

    return fruit


@app.get("/fruits/{fruit_id}", response_model=Fruit)
def get_fruit_by_id(fruit_id: int):
    fruit = get_fruit(fruit_id)

    if fruit is None:
        raise HTTPException(status_code=404, detail="Fruit not found")

    return fruit


@app.put("/fruits/{fruit_id}", response_model=Fruit)
def put_fruit(fruit_id: int, fruit: FruitUpdate):
    updated_fruit = update_fruit(fruit_id, fruit)

    if updated_fruit is None:
        raise HTTPException(status_code=404, detail="Fruit not found")

    return updated_fruit


@app.delete("/fruits/{fruit_id}", status_code=204)
def remove_fruit(fruit_id: int):
    deleted = delete_fruit(fruit_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Fruit not found")

    return Response(status_code=204)