# Ukraine Trip Backend

Сервіс для створення туристичних маршрутів Україною 🗺️

## Опис

Це backend API для додатку Ukraine Trip, створений з використанням FastAPI та SQLAlchemy. Проект використовує Neon як хмарну базу даних PostgreSQL.

## Вимоги

- Python 3.8 або вище
- Git
- Обліковий запис Neon (для бази даних)

## Встановлення

### 1. Клонування репозиторію

```bash
git clone <repository-url>
cd ukraine-trip-backend
```

### 2. Створення віртуального середовища

```bash
python -m venv .venv
```

### 3. Активація віртуального середовища

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Встановлення залежностей

```bash
pip install -e .
```

## Налаштування

### 1. Змінні середовища

Створіть або відредагуйте файл `.env` у корені проекту:

```env
DATABASE_URL=postgresql://username:password@host/database?sslmode=require
SECRET_KEY=your-super-secret-key-here-generate-a-random-one
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Примітка:** Для `SECRET_KEY` використовуйте випадковий рядок довжиною 32+ символів. Ви можете згенерувати його командою:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. CORS налаштування

За замовчуванням додаток налаштований для роботи з frontend на `http://localhost:5173`. Якщо ваш frontend працює на іншій адресі, відредагуйте `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "your-frontend-url"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Після налаштування `.env` файлу, застосуйте міграції бази даних:

```bash
# Активація віртуального середовища (якщо не активоване)
.venv\Scripts\activate  # Windows
# або
source .venv/bin/activate  # Linux/Mac

# Застосування міграцій
alembic upgrade head
```

**Примітка:** Переконайтеся, що ваша Neon база даних створена та доступна.

## Запуск додатку

### Розробка

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Додаток буде доступний за адресою: http://localhost:8000

### Продакшн

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Документація

Після запуску додатку, документація API буде доступна за адресами:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## Структура проекту

```
ukraine-trip-backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── crud/
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   ├── schemas/
│   └── services/
├── alembic/
│   ├── versions/
│   └── env.py
├── .env
├── pyproject.toml
├── alembic.ini
└── README.md
```

## Основні ендпоінти

- `GET /` - Корінь додатку
- `GET /health` - Перевірка здоров'я
- `POST /api/v1/auth/login` - Авторизація
- `POST /api/v1/users/` - Реєстрація користувача
- `GET /api/v1/trips/` - Отримання маршрутів
- `POST /api/v1/trips/` - Створення маршруту

## Розробка

### Створення нових міграцій

Після змін у моделях:

```bash
alembic revision --autogenerate -m "Опис змін"
alembic upgrade head
```

### Тестування

```bash
# Запуск тестів (якщо є)
pytest
```

## Розгортання

Для розгортання на сервері рекомендується використовувати:

- Gunicorn + Uvicorn workers
- Nginx як reverse proxy
- Docker (якщо потрібно контейнеризація)

## Ліцензія

[Вкажіть ліцензію проекту]

## Контакти

[Контактна інформація]</content>
<parameter name="filePath">c:\Users\dmytr\OneDrive\Desktop\ukraine-trip-backend\README.md