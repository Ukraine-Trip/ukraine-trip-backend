# Використовуємо офіційний легкий образ Python
FROM python:3.12-slim

WORKDIR /app

# Забороняємо Python створювати зайві кеш-файли
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Оновлюємо pip (гарна практика)
RUN pip install --upgrade pip

# Спочатку копіюємо файли конфігурації проєкту (для кешування Докером)
COPY pyproject.toml README.md ./

# Копіюємо код (потрібно для того, щоб pip install . спрацював коректно)
COPY src/ ./src/

# Встановлюємо залежності проєкту з pyproject.toml
RUN pip install --no-cache-dir .

# Копіюємо всі інші файли (наприклад, alembic, тести тощо)
COPY . .

# Запускаємо сервер
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]