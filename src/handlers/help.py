from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def cmd_ping(message: Message):
    message_text="""
/start - start bot
/stats - get stats about vaults
/help - get help
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Start", callback_data="start"),
        ],
        [
            InlineKeyboardButton(text="Stats", callback_data="stats")
        ]
    ])
    await message.answer(message_text,reply_markup=keyboard)
