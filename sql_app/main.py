from typing import List
import uuid

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/inventario", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.post("/inventario/{id_carrinho}", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate,id_carrinho: uuid.UUID, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item,carrinho_id=id_carrinho)

@app.delete("/inventario/{item_id}")
def delete_item(item_id: uuid.UUID, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(db=db, item_id=item_id)
    if db_item:
        return crud.delete_item(db=db, item=db_item)
    else:
        return HTTPException(status_code=404)

# ------ carrinho ------ #

@app.post("/carrinho", response_model=schemas.Carrinho)
def add_carrinho(carrinho : schemas.CarrinhoCreate, db: Session =Depends(get_db)):
    return crud.create_carrinho(db=db, carrinho=carrinho)

@app.delete("/carrinho/{id_carrinho}")
def delete_carrinho(id_carrinho: uuid.UUID, db: Session = Depends(get_db)):
    db_carrinho = crud.get_carrinho_by_id(db=db, id_carrinho=id_carrinho)
    if db_carrinho:
        return crud.delete_carrinho(db=db, id_carrinho=id_carrinho)
    else:
        return HTTPException(status_code=404)

@app.get("/carrinhos", response_model=List[schemas.Carrinho])
def read_carrinhos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    carrinhos = crud.get_carrinhos(db=db, skip=skip,limit=limit)
    return carrinhos

@app.get("/carrinho/{id_carrinho}", response_model=schemas.Carrinho)
def read_carrinho(id_carrinho: uuid.UUID, db: Session = Depends(get_db)):
    db_carrinho = crud.get_carrinho_by_id(db, id_carrinho=id_carrinho)
    if db_carrinho is None:
        raise HTTPException(status_code=404, detail="Carrinho not found")
    return db_carrinho