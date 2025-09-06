from DB.managers.base_manager import BaseAlchemyManager
from sqlalchemy.dialects.postgresql import insert
from DB.models import AlchemyUsers
from sqlalchemy import select, update, func, and_
from datetime import datetime, timezone, timedelta

class UserManager(BaseAlchemyManager):
    """Manager class for user operations."""

    async def create_user_if_not_exist(self, user_id: int, username: str):
        stmt = (
            insert(AlchemyUsers)
            .values(
                telegram_id=user_id,
                username=username,
                is_notified=False
            )
            .on_conflict_do_nothing(index_elements=[AlchemyUsers.telegram_id])
            .returning(AlchemyUsers)
        )

        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            # достаём уже существующего пользователя

            stmt_select = select(AlchemyUsers).where(AlchemyUsers.telegram_id == user_id)
            result = await self.session.execute(stmt_select)
            user = result.scalar_one()

        await self.session.commit()
        return user

    async def toggle_notifications(self, user_id: int):
        # Получаем текущего пользователя
        stmt_select = select(AlchemyUsers).where(AlchemyUsers.telegram_id == user_id)
        result = await self.session.execute(stmt_select)
        user = result.scalar_one_or_none()

        if not user:
            return None  # если такого пользователя нет

        # Инвертируем значение
        new_value = not user.is_notified

        # Обновляем запись в базе
        stmt_update = (
            update(AlchemyUsers)
            .where(AlchemyUsers.telegram_id == user_id)
            .values(is_notified=new_value)
            .returning(AlchemyUsers)
        )

        result = await self.session.execute(stmt_update)
        updated_user = result.scalar_one()
        await self.session.commit()

        return updated_user

    async def update_limit(self,user_id: int, new_limit: float):
        stmt_select = select(AlchemyUsers).where(AlchemyUsers.telegram_id == user_id)
        result = await self.session.execute(stmt_select)
        user = result.scalar_one_or_none()

        if not user:
            return None  # если такого пользователя нет

        stmt_update = (
            update(AlchemyUsers)
            .where(AlchemyUsers.telegram_id == user_id)
            .values(limit=new_limit)
            .returning(AlchemyUsers)
        )

        result = await self.session.execute(stmt_update)
        updated_user = result.scalar_one()
        await self.session.commit()

        return updated_user

    async def get_and_update_users_for_notification(self,value: float = 15000000) -> list[AlchemyUsers]:
        """Get users for notification and update their last_time_notified."""
        now_utc = datetime.utcnow()
        five_minutes_ago = now_utc - timedelta(seconds=300)

        stmt_select = (
            select(AlchemyUsers)
            .where(
                and_(
                    AlchemyUsers.is_notified == True,
                    AlchemyUsers.last_time_notified <= five_minutes_ago,
                    AlchemyUsers.limit > 0,
                    AlchemyUsers.limit < value
                )
            )
            .order_by(AlchemyUsers.last_time_notified.asc())
        )

        # Получаем пользователей
        result = await self.session.execute(stmt_select)
        users = result.scalars().all()

        if not users:
            return []

        # Обновляем last_time_notified на текущее время
        user_ids = [user.telegram_id for user in users]
        stmt_update = (
            update(AlchemyUsers)
            .where(AlchemyUsers.telegram_id.in_(user_ids))
            .values(last_time_notified=now_utc)
            .returning(AlchemyUsers)
        )
        result_update = await self.session.execute(stmt_update)
        await self.session.commit()

        updated_users = result_update.scalars().all()
        return updated_users