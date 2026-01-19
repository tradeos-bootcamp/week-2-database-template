from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Схема для создания товара
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, example="Ноутбук HP")
    price: float = Field(..., gt=0, example=75000.0)
    quantity: int = Field(default=0, ge=0, example=10)
    category: Optional[str] = Field(None, max_length=100, example="электроника")
    description: Optional[str] = Field(None, example="Мощный игровой ноутбук")

# Схема для обновления товара
class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)

# Схема для ответа с товаром
class Product(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    category: Optional[str]
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True  # Ранее было orm_mode=True