import sys
import asyncio # Додали asyncio
from os.path import abspath, dirname
from logging.config import fileConfig
#from src.app.core.config import settings
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine # Додали асинхронний двигун
from alembic import context



sys.path.insert(0, dirname(dirname(abspath(__file__))))

from src.app.models import Base 

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Твій хардкод URL для локальної бази
DB_URL = "postgresql+asyncpg://user:password@db:5432/ukraine_trip"

def run_migrations_offline() -> None:
    """Офлайн міграції."""
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "pyformat"},
    )
    with context.begin_transaction():
        context.run_migrations()

# --- НОВИЙ АСИНХРОННИЙ БЛОК ---

def do_run_migrations(connection):
    """Ця функція виконується всередині синхронного контексту."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """Асинхронне підключення до бази."""
    connectable = create_async_engine(
        DB_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Конвертуємо асинхронне підключення в синхронне для Alembic
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Точка входу для онлайн міграцій."""
    asyncio.run(run_async_migrations())

# ------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()