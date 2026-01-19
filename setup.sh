#!/bin/bash
echo "🚀 Настройка проекта недели 2..."

# Создаем виртуальное окружение
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows

# Устанавливаем зависимости
pip install -r requirements.txt

# Инициализируем Alembic
alembic init migrations

# Обновляем env.py
echo "Обновите файл migrations/env.py как указано в README.md"

# Создаем первую миграцию
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

echo "✅ Настройка завершена!"
echo "Запустите: docker-compose up --build"