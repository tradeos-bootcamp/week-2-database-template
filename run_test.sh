#!/bin/bash
echo "🧪 Запуск тестов..."

# Активируем venv если есть
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Запускаем тесты
pytest tests/ -v

echo "✅ Тесты завершены!"