from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# temporary in-memory storage
items = []

# model
class Item(BaseModel):
    id: int
    name: str
    price: float


# CREATE
@app.post("/items", response_model=Item)
def create_item(item: Item):
    items.append(item)
    return item


# READ ALL
@app.get("/items", response_model=List[Item])
def get_items():
    return items


# READ ONE
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


# UPDATE
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items):
        if item.id == item_id:
            items[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")


# DELETE
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for index, item in enumerate(items):
        if item.id == item_id:
            deleted_item = items.pop(index)
            return {"message": "Item deleted", "data": deleted_item}
    raise HTTPException(status_code=404, detail="Item not found")