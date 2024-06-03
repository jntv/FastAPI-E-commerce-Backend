from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, Float, String, UniqueConstraint
from database.connection import Base
class Product(Base):
    __tablename__ = "Products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
