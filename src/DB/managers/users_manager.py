from DB.managers.base_manager import BaseAlchemyManager
from sqlalchemy.dialects.postgresql import insert

from DB.models import AlchemyUsers


class UserManager(BaseAlchemyManager):
    """Manager class for user operations."""
    async def create_user_if_not_exist(self,user_id:int,username:str):
        stmt = (
            insert(AlchemyUsers)
            .values(telegram_id=user_id, username=username)
            .on_conflict_do_nothing(index_elements=[AlchemyUsers.telegram_id])
            .returning(AlchemyUsers)
        )
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        await self.session.commit()
        return user