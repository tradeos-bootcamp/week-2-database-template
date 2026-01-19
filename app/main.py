from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas, crud
from app.database import engine, get_db

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TradeOS Product API",
    description="API для управления товарами с PostgreSQL",
    version="2.0.0"
)

@app.get("/", tags=["Информация"])
async def root():
    """Корневой endpoint с информацией о API"""
    return {
        "message": "Добро пожаловать в TradeOS Product API",
        "version": "2.0.0",
        "description": "API для управления товарами с PostgreSQL",
        "docs": "/docs",
        "health_check": "/health"
    }

@app.get("/health", tags=["Мониторинг"])
async def health_check(db: Session = Depends(get_db)):
    """Проверка работоспособности API и подключения к БД"""
    try:
        # Проверяем подключение к БД
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "ok",
        "database": db_status,
        "service": "tradeos-product-api"
    }

@app.get("/products", response_model=List[schemas.Product], tags=["Товары"])
async def read_products(
    skip: int = Query(0, ge=0, description="Пропустить первые N записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    min_price: Optional[float] = Query(None, ge=0, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, ge=0, description="Максимальная цена"),
    db: Session = Depends(get_db)
):
    """Получить список товаров с пагинацией и фильтрацией"""
    products = crud.get_products(
        db, 
        skip=skip, 
        limit=limit,
        category=category,
        min_price=min_price,
        max_price=max_price
    )
    return products

@app.get("/products/{product_id}", response_model=schemas.Product, tags=["Товары"])
async def read_product(product_id: int, db: Session = Depends(get_db)):
    """Получить товар по ID"""
    product = crud.get_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

@app.post("/products", response_model=schemas.Product, tags=["Товары"], status_code=201)
async def create_product(
    product: schemas.ProductCreate, 
    db: Session = Depends(get_db)
):
    """Создать новый товар"""
    return crud.create_product(db=db, product=product)

@app.put("/products/{product_id}", response_model=schemas.Product, tags=["Товары"])
async def update_product(
    product_id: int,
    product_update: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):
    """Обновить существующий товар"""
    product = crud.update_product(db=db, product_id=product_id, product_update=product_update)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

@app.delete("/products/{product_id}", tags=["Товары"])
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Удалить товар"""
    success = crud.delete_product(db=db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return {"message": "Товар успешно удален", "product_id": product_id}