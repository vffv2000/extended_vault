import asyncio
import functools
from contextlib import asynccontextmanager
from typing import Any, Callable, Coroutine

from sqlalchemy import MetaData, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from typing_extensions import AsyncGenerator

from core.config import settings
from core.custom_logs import log


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models.

    All other models should inherit from this class.
    """

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


async_engine = create_async_engine(settings.get_database_connection_string, echo=False,
                                   pool_size=10,
                                   max_overflow=20
                                   )
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    """Get a database session.

    To be used for dependency injection.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()



def decorate_all_methods(decorator):
    def decorate(cls):
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and asyncio.iscoroutinefunction(attr_value):
                setattr(cls, attr_name, decorator(attr_value))
        return cls

    return decorate


def handle_exceptions(
        func: Callable[..., Coroutine[Any, Any, Any]]
) -> Callable[..., Coroutine[Any, Any, Any]]:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            log.error(f"Ошибка в методе {func.__name__}: {e}", exc_info=True)
            error_msg = f"Error in database: {e}"
            raise RuntimeError(error_msg) from e

    return wrapper


def sync_auto_increment(table_name: str, column_name: str):
    """Декоратор для синхронизации автоинкремента для любых таблиц и колонок."""

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            await self.session.execute(
                text(
                    f"SELECT setval(pg_get_serial_sequence('{table_name}', '{column_name}'), max({column_name})) FROM {table_name}"
                )
            )
            return await func(self, *args, **kwargs)

        return wrapper

    return decorator

