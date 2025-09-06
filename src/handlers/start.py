from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from DB.managers.users_manager import UserManager
from DB.sqlalchemy_database_manager import async_session
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from core.config import settings
from texts.texts import build_start_text, build_start_keyboard, INPUT_NUMBER_TEXT, INPUT_NUMBER_ERROR, \
    INPUT_NUMBER_ERROR_2

router = Router()


class LimitStates(StatesGroup):
    waiting_for_limit = State()


@router.callback_query(lambda c: c.data == "start")
async def cb_toggle_notify(callback: CallbackQuery, state: FSMContext):
    await settings.telegram_bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await handle_start(callback.from_user.id, callback.from_user.username)
    await callback.answer()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    await handle_start(user_id,username)


async def handle_start(user_id,username):
    async with async_session() as session:
        user_manager = UserManager(session)
        user = await user_manager.create_user_if_not_exist(user_id, username)

    user_status = user.is_notified

    text = await build_start_text(status=user_status,limit=user.limit)
    await settings.telegram_bot.send_message(chat_id=user_id,text=text,
                                             reply_markup=await build_start_keyboard(user_status),
                                             parse_mode=ParseMode.HTML )




@router.callback_query(lambda c: c.data == "toggle_notify")
async def toggle_notify_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with async_session() as session:
        user_manager = UserManager(session)
        user = await user_manager.toggle_notifications(user_id)  # switches is_notified

    user_status=user.is_notified

    text= await build_start_text(status=user_status,limit=user.limit)
    await callback.message.edit_text(
        text=text,
        reply_markup=await build_start_keyboard(user.is_notified),
        parse_mode=ParseMode.HTML
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "set_limit")
async def set_limit_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(LimitStates.waiting_for_limit)

    await state.update_data(bot_message_id=callback.message.message_id)
    await callback.message.edit_text(INPUT_NUMBER_TEXT)
    await callback.answer()


@router.message(LimitStates.waiting_for_limit)
async def process_limit(message: Message, state: FSMContext):
    data = await state.get_data()
    bot_message_id = data.get("bot_message_id")

    # сразу удаляем сообщение пользователя
    try:
        await message.delete()
    except Exception:
        pass  # если вдруг нет прав на удаление

    try:
        new_limit = float(message.text)
    except ValueError:
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=bot_message_id,
            text=INPUT_NUMBER_ERROR
        )
        return

    if new_limit <= 0 or new_limit >= 100000:
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=bot_message_id,
            text=INPUT_NUMBER_ERROR_2
        )
        return


    user_id = message.from_user.id
    async with async_session() as session:
        user_manager = UserManager(session)
        user = await user_manager.update_limit(user_id, new_limit)
    text = await build_start_text(status=user.is_notified,limit=user.limit)

    await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=bot_message_id,
        text=text,
        reply_markup=await build_start_keyboard(user.is_notified),parse_mode=ParseMode.HTML
    )
    await state.clear()
