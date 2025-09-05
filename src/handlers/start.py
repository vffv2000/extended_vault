from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from DB.managers.users_manager import UserManager
from DB.sqlalchemy_database_manager import async_session

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    async with async_session() as session:
        user_manager = UserManager(session)
        await user_manager.create_user_if_not_exist(user_id, username)
    await message.answer("👋 Привет! Я бот для алертов по funding.")
