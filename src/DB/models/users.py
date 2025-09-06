
from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, func, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import BigInteger
from DB.sqlalchemy_database_manager import Base


class AlchemyUsers(Base):
    __tablename__ = "users"

    telegram_id = Column(BigInteger, primary_key=True)
    username = Column(String(50), nullable=True)
    limit = Column(Numeric(30, 0))
    last_time_notified = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    is_notified = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

