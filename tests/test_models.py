import pytest
from app.models import Product
from datetime import datetime

def test_create_product():
    """Тест создания модели Product"""
    product = Product(
        id=1,
        name="Тестовый товар",
        price=100.0,
        quantity=10,
        category="тест",
        description="Тестовое описание"
    )
    
    assert product.id == 1
    assert product.name == "Тестовый товар"
    assert product.price == 100.0
    assert product.quantity == 10
    assert product.category == "тест"
    assert product.description == "Тестовое описание"
    assert isinstance(product.created_at, datetime)
    
def test_product_repr():
    """Тест строкового представления модели"""
    product = Product(id=1, name="Тест", price=50.0)
    repr_str = repr(product)
    assert "Product" in repr_str
    assert "id=1" in repr_str
    assert "name='Тест'" in repr_str
