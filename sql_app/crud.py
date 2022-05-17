from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null
from . import models, schemas
from fastapi import HTTPException, status


def get_carrinho_by_id(db: Session, id_carrinho: int):
    return db.query(models.Carrinho).filter(models.Carrinho.id == id_carrinho).first()


def get_carrinhos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Carrinho).offset(skip).limit(limit).all()


def create_carrinho(db: Session, carrinho: schemas.CarrinhoCreate):
    db_carrinho = models.Carrinho(items=carrinho.Items)
    db.add(db_carrinho)
    db.commit()
    db.refresh(db_carrinho)
    return db_carrinho

def get_item_by_id(db: Session, carrinho_id: int , skip: int = 0):
    return db.query(models.Item).filter(models.Item.carrinho_id == carrinho_id).offset(skip).all()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate, carrinho_id):
    db_item = models.Item(**item.dict(), carrinho_id=carrinho_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_carrinho(db: Session, carrinho_id: int, carrinho: schemas.CarrinhoCreate):
    carrinho_to_update=db.query(models.Carrinho).filter(models.Carrinho.id==carrinho_id).first()
    carrinho_to_update.items = carrinho.items
    db.commit()

    return carrinho_to_update

def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    item_to_update=db.query(models.Item).filter(models.Item.id==item_id).first()
    item_to_update.carrinho_id=item.carrinho_id
    item_to_update.name=item.name
    item_to_update.price=item.price

    db.commit()
    return item_to_update

def delete_carrinho(db: Session,  carrinho: schemas.Carrinho):
    carrinho_to_delete=db.query(models.Carrinho).filter(models.Carrinho.id==carrinho.id).first()
    items = get_items(db=db, carrinho_id=carrinho.id)

    if carrinho_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Carrinho não encontrado!")
    
    db.delete(carrinho_to_delete)
    db.commit()
    
    return carrinho_to_delete

def delete_item(db: Session,  item: schemas.Item, carrinho: schemas.Carrinho):
    item_to_delete=db.query(models.Item).filter(models.Item.carrinho_id==carrinho.id).first()

    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item não encontrado!")

    db.delete(item_to_delete)
    db.commit()

    return item_to_delete