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

# ----todo
@app.patch("/inventario/{item_id}")
def update_item(item_id: uuid.UUID, item: Item):
    try:
        base["inventario"][item_id] = item
        return base["inventario"]
    except:
        raise HTTPException(status_code=404)
# ----



@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
