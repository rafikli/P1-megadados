# SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database.

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Carrinho(Base):
    __tablename__ = "carrinhos"
    id = Column(Integer, primary_key=True, index=True)

    items = relationship("Item", back_populates="carrinhos", cascade="all, delete-orphan")
    
    
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    carrinho_id = Column(Integer, ForeignKey("carrinhos.id"))
    name = Column(String(50), unique=True, index=True)
    price = Column(Integer, index=True)
    carrinhos = relationship("Cart", back_populates="items")
