
from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, func, UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship

from DB.sqlalchemy_database_manager import Base

class AlchemyVaults(Base):
    __tablename__ = "vaults"

    id= Column(BIGINT, primary_key=True)
    equity = Column(Numeric(20, 6))
    wallet_balance = Column(Numeric(20, 6))
    last_30_days_apr = Column(Numeric(10, 5))
    exposure = Column(Numeric(25, 6))
    numberOfDepositors = Column(Integer)
    age_days = Column(Integer)
    profit_share = Column(Numeric(10, 5))

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)