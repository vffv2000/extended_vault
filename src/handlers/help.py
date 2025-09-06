from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from texts.texts import build_help_keyboard, HELP_TEXT

router = Router()

@router.message(Command("help"))
async def cmd_ping(message: Message):
    await message.answer(HELP_TEXT,reply_markup=await build_help_keyboard())
