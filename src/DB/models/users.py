
from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, func, UniqueConstraint
from sqlalchemy.orm import relationship

from DB.sqlalchemy_database_manager import Base


class AlchemyUsers(Base):
    __tablename__ = "users"

    telegram_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

