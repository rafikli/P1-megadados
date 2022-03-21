from ast import excepthandler
from re import I
from typing import Optional, List
from fastapi import FastAPI, HTTPException

from pydantic import BaseModel
import uuid

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float 

class Carrinho(BaseModel):
    id_user: uuid.UUID
    itens: dict 

@app.get("/")
def read_root():
    return {"Hello": "World"}

base = {
    "carrinho" : {},
    "inventario" : {}
}   

@app.get("/inventario")
def read_item():
    return base["inventario"]

@app.post("/inventario")
def create_item(item : Item):
    try:
        id = uuid.uuid1()
        base["inventario"][id] = item
        
        return base["inventario"]
    except:
        raise HTTPException(status_code=400)

@app.patch("/inventario/{item_id}")
def update_item(item_id: uuid.UUID, item: Item):
    base["inventario"][item_id] = item
    return base["inventario"]

@app.delete("/inventario/{item_id}")
def delete_item(item_id: uuid.UUID):
    print(base["inventario"])
    if item_id not in base["inventario"]:
        raise HTTPException(status_code=404)  
    else:
        base["inventario"].pop(item_id,False)
        return base["inventario"]
