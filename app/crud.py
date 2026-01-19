from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app import models, schemas

# CRUD операции для Product

def get_product(db: Session, product_id: int):
    """Получить товар по ID"""
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    """Получить список товаров с фильтрацией"""
    query = db.query(models.Product)
    
    # Применяем фильтры если указаны
    if category:
        query = query.filter(models.Product.category == category)
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)
    
    return query.order_by(desc(models.Product.created_at)).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    """Создать новый товар"""
    db_product = models.Product(
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        category=product.category,
        description=product.description
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: schemas.ProductUpdate):
    """Обновить существующий товар"""
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    
    update_data = product_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    """Удалить товар"""
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    
    db.delete(db_product)
    db.commit()
    return True