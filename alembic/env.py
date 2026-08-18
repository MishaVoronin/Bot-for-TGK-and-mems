import asyncio
import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# 1. Загружаем переменные окружения
load_dotenv()

config = context.config

# 2. Берем URL из .env (должен быть postgresql+asyncpg://...)
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Импортируем Base и ВСЕ модели, чтобы Alembic их видел
# Убедись, что пути правильные для твоей структуры
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.db import Base
from src.models import Message  # <-- ЗАМЕНИ НА СВОИ РЕАЛЬНЫЕ МОДЕЛИ

target_metadata = Base.metadata


# 4. Асинхронная функция для применения миграций
def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# 5. Запускаем асинхронный цикл
if context.is_offline_mode():
    raise Exception("Offline mode not supported for async Alembic")
else:
    asyncio.run(run_migrations_online())
