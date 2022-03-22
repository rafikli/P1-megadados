from ast import excepthandler
from typing import Optional, List
from fastapi import FastAPI, HTTPException, status

from pydantic import BaseModel
import uuid

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float 
    quantity:  Optional[int]

class Carrinho(BaseModel):
    id_user: int
    items: dict 

base = {
    "carrinho" : {},
    "inventario" : {},
    "usuario" : {}
}   

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/inventario")
def read_item():
    return base["inventario"]

@app.post("/inventario", status_code = 201)
def create_item(item : Item):
    try:
        id = uuid.uuid1()
        base["inventario"][id] = item
        return base["inventario"]
    except:
        raise HTTPException(status_code=400)

@app.patch("/inventario/{item_id}")
def update_item(item_id: uuid.UUID, item: Item):
    try:
        base["inventario"][item_id] = item
        return base["inventario"]
    except:
        raise HTTPException(status_code=404)
        
@app.delete("/inventario/{item_id}")
def delete_item(item_id: uuid.UUID):
    try:
        print(base["inventario"])
        if item_id not in base["inventario"]:
            raise HTTPException(status_code=404)  
        else:
            base["inventario"].pop(item_id,False)
            return base["inventario"]
    except:
         raise HTTPException(status_code=404)

# ------ carrinho ------ #

@app.post("/carrinho")
def add_carrinho(carrinho : Carrinho):
    try:
        id = uuid.uuid1()
        base["carrinho"][id] = carrinho
        return base["carrinho"]
    except:
        raise HTTPException(status_code=404)

@app.delete("/carrinho/{id_carrinho}")
def delete_carrinho(id_carrinho: uuid.UUID):
    try:
        if id_carrinho not in base["carrinho"]:
            raise HTTPException(status_code=404)  
        else:
            base["carrinho"].pop(id_carrinho,False)
            return base["carrinho"]
    except:
        raise HTTPException(status_code=404)

@app.get("/carrinhos")
def read_carrinhos():
    return base["carrinho"]
    
@app.get("/carrinho/{id_carrinho}")
def read_carrinho(id_carrinho : uuid.UUID):
    try:
        return base["carrinho"][id_carrinho]
    except:
        raise HTTPException(status_code=404)

@app.post("/carrinho/{id_carrinho}/{id_item}", status_code = 201)
def update_item_carrinho(id_carrinho: uuid.UUID, id_item: uuid.UUID, item: Item):
    try:
        if id_carrinho not in base["carrinho"]:
            raise HTTPException(status_code=404, detail="Carrinho not found")

        if id_item not in base["inventario"]:
            raise HTTPException(status_code=404, detail="Item not found")

        if id_item not in base["carrinho"][id_carrinho].items.keys():
            base["carrinho"][id_carrinho].items.update({ id_item: item })

        else:   
            base["carrinho"][id_carrinho].items[id_item].quantity += item.quantity
        return base["carrinho"]
    except:
        raise HTTPException(status_code=404)

@app.delete("/carrinho/{id_carrinho}/{id_item}")
def delete_item_carrinho(id_carrinho: uuid.UUID, id_item: uuid.UUID, item: Item):
    try:
        if id_carrinho not in base["carrinho"]:
            raise HTTPException(status_code=404)

        if id_item not in base["inventario"]:
            raise HTTPException(status_code=404)

        if id_item not in base["carrinho"][id_carrinho].items.keys():
            raise HTTPException(status_code=404)

        else:   
            base["carrinho"][id_carrinho].items[id_item].quantity -= item.quantity

            if  base["carrinho"][id_carrinho].items[id_item].quantity <= 0:
                base["carrinho"][id_carrinho].items.pop(id_item, False)
            
        return base["carrinho"]
    except:
        raise HTTPException(status_code=404)