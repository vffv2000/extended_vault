

from DB.managers.base_manager import BaseAlchemyManager
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from DB.models import AlchemyUsers
from DB.models.vaults import AlchemyVaults
from datetime import datetime
from typing import List

class VaultsManager(BaseAlchemyManager):
    """Manager class for user operations."""
    async def get_last_vaults(self, limit: int = 10)-> list[AlchemyVaults]:
        stmt = select(AlchemyVaults).order_by(AlchemyVaults.created_at.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_last_vault(self) -> AlchemyVaults | None:
        stmt = select(AlchemyVaults).order_by(AlchemyVaults.created_at.desc()).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def upload_vaults_data(
        self,
        equity: float,
        wallet_balance: float,
        last_30_days_apr: float,
        exposure: float,
        numberOfDepositors: int,
        age_days: int,
        profit_share: float
    ):
        stmt = insert(AlchemyVaults).values(
            equity=equity,
            wallet_balance=wallet_balance,
            last_30_days_apr=last_30_days_apr,
            exposure=exposure,
            numberOfDepositors=numberOfDepositors,
            age_days=age_days,
            profit_share=profit_share
        ).returning(AlchemyVaults)

        result = await self.session.execute(stmt)
        vault = result.scalar_one_or_none()
        await self.session.commit()
        return vault

    async def get_vaults_since(self, cutoff: datetime) -> List[AlchemyVaults]:
        """
        Get all vault records created since the given cutoff datetime.

        :param cutoff: datetime, return records where created_at >= cutoff
        :return: list of AlchemyVaults
        """
        stmt = select(AlchemyVaults).where(AlchemyVaults.created_at >= cutoff).order_by(AlchemyVaults.created_at.asc())
        result = await self.session.execute(stmt)
        return result.scalars().all()