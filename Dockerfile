FROM python:3.12-slim

# Встановлюємо залежності для psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Копіюємо конфігурацію
COPY pyproject.toml .

# КРИТИЧНО: Створюємо пустий README, бо pip install . часто його шукає
RUN touch README.md

# Оновлюємо pip і встановлюємо проєкт
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Копіюємо код
COPY ./app ./app

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
