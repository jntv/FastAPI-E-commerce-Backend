from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from ..auth.models import User
from . import models
from ..auth.auth_endpoints import get_current_user
from database import connection

router = APIRouter(prefix="/api/orders")


class OrderItem(BaseModel):
    product_id: int
    quantity: int


class Order(BaseModel):
    user_email: EmailStr
    items: list[OrderItem]
    total: Optional[float] = None  # Can be calculated on the server-side

@router.get("/", tags=["Orders"])
async def get_all_orders(db: Session = Depends(connection.get_db), current_user: User = Depends(get_current_user)):
    orders = db.query(models.Order).filter(models.Order.user_email == current_user.email).all()
    return orders


@router.post("/create_order", tags=["Orders"])
async def create_order(order_req: Order, db: Session = Depends(connection.get_db), current_user: User = Depends(get_current_user)):
    # Validate product existence and quantities
    for item in order_req.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product or product.quantity < item.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid product or quantity")
        
    # total price calculate
    total_order_price = 0
    for item in order_req.items:
        total_order_price += product.price
        
        
    for item in order_req.items:
        new_order = models.Order(user_email=current_user.email, total=total_order_price)
        db.add(new_order)
        db.commit()
    order = db.query(models.Order).filter(models.Order.user_email == current_user.email).first()
    # Reduce product quantity, calcualte total_order_price based on order items
    for item in order_req.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        product.quantity -= item.quantity
        db.add(product)
    
        db.commit()
    for item in order_req.items:
        order_item = models.OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity)
        db.add(order_item)
        
    return {"message": f"Order was created successfully for {total_order_price} for user {current_user.email}."}


@router.get("/get_order/{order_id}", tags=["Orders"])
async def get_order(order_id: int, db: Session = Depends(connection.get_db), current_user: User = Depends(get_current_user)):
    # Check if order belongs to current user
    order = db.query(models.Order).filter(models.Order.id == order_id, models.Order.user_email == current_user.email).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.put("/update_order/{order_id}", tags=["Orders"])
async def update_order(order_id: int, updated_order: Order, db: Session = Depends(connection.get_db), current_user: User = Depends(get_current_user)):
    # Check if order belongs to current user
    order = db.query(models.Order).filter(models.Order.id == order_id, models.Order.user_email == current_user.email).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    # Update order details (implement based on your requirements
    order.items = updated_order.items
    order.total = updated_order.total  # Update total if needed

    db.add(order)
    db.commit()
    return order


@router.delete("/delete_order{order_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Orders"])
async def delete_order(order_id: int, db: Session = Depends(connection.get_db), current_user: User = Depends(get_current_user)):
    # Check if order belongs to current user
    order = db.query(models.Order).filter(models.Order.id == order_id, models.Order.user_email == current_user.email).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}