from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from pydantic import BaseModel

# Define a router
router = APIRouter()

# Example Pydantic model for request and response
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

# In-memory storage for items
items = []

@router.get("/items", response_model=List[Item])
async def read_items():
    return items

@router.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    items.append(item)
    return item

@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id >= len(items) or item_id < 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id >= len(items) or item_id < 0:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    return item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    if item_id >= len(items) or item_id < 0:
        raise HTTPException(status_code=404, detail="Item not found")
    items.pop(item_id)
    return None

