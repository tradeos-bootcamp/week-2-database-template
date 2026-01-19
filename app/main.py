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

# TODO: Добавить CRUD endpoint'ы для товаров
# GET /products
# GET /products/{id}
# POST /products
# PUT /products/{id}
# DELETE /products/{id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
