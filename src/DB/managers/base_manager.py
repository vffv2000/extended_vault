"""Base manager class for SQLAlchemy database operations."""
from sqlalchemy.ext.asyncio import AsyncSession

from DB.sqlalchemy_database_manager import decorate_all_methods, handle_exceptions


class ManagerMeta(type):
    """Metaclass that automatically decorates all methods of the class with the `handle_exceptions` decorator.

    This allows centralized error handling across all manager classes
    that inherit from `BaseAlchemyManager` without needing to explicitly
    decorate each method.
    """

    def __new__(cls, name, bases, dct):
        """Create a new class instance and applies the `handle_exceptions."""
        new_cls = super().__new__(cls, name, bases, dct)
        return decorate_all_methods(handle_exceptions)(new_cls)


class BaseAlchemyManager(metaclass=ManagerMeta):
    """Base class for all database managers using SQLAlchemy.

    Automatically applies exception handling to all public methods
    via the `ManagerMeta` metaclass.

    :param session: SQLAlchemy asynchronous session instance.
    :type session: AsyncSession
    """

    def __init__(self, session: AsyncSession):
        """Initialize the base manager with an SQLAlchemy session."""
        self.session = session
