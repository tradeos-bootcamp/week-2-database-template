import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import crud, schemas

# Тестовая база данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """Создание тестовой БД для каждого теста"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_product(db):
    """Тест создания товара"""
    product_data = schemas.ProductCreate(
        name="Тестовый товар",
        price=100.0,
        quantity=5,
        category="тест"
    )
    
    product = crud.create_product(db, product_data)
    
    assert product.id is not None
    assert product.name == "Тестовый товар"
    assert product.price == 100.0
    assert product.quantity == 5
    assert product.category == "тест"

def test_get_product(db):
    """Тест получения товара"""
    # Сначала создаем
    product_data = schemas.ProductCreate(name="Товар", price=50.0)
    created = crud.create_product(db, product_data)
    
    # Потом получаем
    retrieved = crud.get_product(db, created.id)
    
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.name == "Товар"
