from typing import List, Union

from pydantic import BaseModel


 
class ItemBase(BaseModel):
    name: str
    price: float 

class ItemCreate(ItemBase):
    pass

class Carrinho(BaseModel):
    id_user: int
    class Config:
        orm_mode = True

class CarrinhoBase(BaseModel):
    items: List[Carrinho] = None 
    pass

class CarrinhoCreate(CarrinhoBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


