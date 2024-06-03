from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import connection
from . import models

router = APIRouter(prefix="/api/products")
class ProductData(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    
@router.get("/", tags=["Products"])
async def get_all_products(db: Session = Depends(connection.get_db)):
    products = db.query(models.Product).all()
    return products

@router.get("/{product_id}", tags=["Products"])
async def get_product(product_id: int, db: Session = Depends(connection.get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.post("/create_product", tags=["Products"])
async def create_product(product: ProductData, db: Session = Depends(connection.get_db)):
    new_product = models.Product(
            name        = product.name,
            description = product.description,
            price       = product.price,  
            quantity    = product.quantity
            )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)  # Refresh object with generated ID
    return product

@router.put("/update_product/{product_id}", tags=["Products"])
async def update_product(product_id: int, updated_product: ProductData, db: Session = Depends(connection.get_db)):
    # Implement optimistic locking (or similar) to handle concurrency
    existing_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    # Update existing product attributes
    existing_product.name = updated_product.name
    existing_product.description = updated_product.description
    existing_product.price = updated_product.price
    db.add(existing_product)
    db.commit()
    return {"message": "Product updated successfully"}

@router.delete("/delete_product", status_code=status.HTTP_204_NO_CONTENT, tags=["Products"])
async def delete_product(product_id: int, db: Session = Depends(connection.get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return {"message": "Product deleted"}
    db.delete(product)
    db.commit()
