import tempfile

from aiogram import types, Router
from aiogram.filters import Command
from datetime import datetime, timedelta
import io
import matplotlib.pyplot as plt
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from DB.sqlalchemy_database_manager import async_session
from DB.managers.vaults_manager import VaultsManager
from core.config import settings
from aiogram.types.input_file import FSInputFile

router = Router()

@router.callback_query(lambda c: c.data == "stats")
async def cb_toggle_notify(callback: CallbackQuery, state: FSMContext):
    await settings.telegram_bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await handle_stats(callback.from_user.id)
    await callback.answer()

@router.message(Command("stats"))
async def cmd_vault_stats(message: types.Message):
    user_id = message.from_user.id
    await handle_stats(user_id)


async def handle_stats(user_id):
    cutoff = datetime.utcnow() - timedelta(hours=24)
    async with async_session() as session:
        vault_manager = VaultsManager(session)
        vaults = await vault_manager.get_vaults_since(cutoff)

    equities = [float(v.equity) for v in vaults]
    times = [v.created_at for v in vaults]

    max_equity = max(equities)
    min_equity = min(equities)
    current_equity = equities[-1]

    text = (
        f"📊 Vault statistics (last 24h):\n"
        f"Max equity: {max_equity}\n"
        f"Min equity: {min_equity}\n"
        f"Current equity: {current_equity}"
    )

    # Создаём график
    plt.figure(figsize=(10, 5))
    plt.plot(times, equities, marker='o', label='Equity', color='blue')
    plt.scatter(times[equities.index(max_equity)], max_equity, color='green', label='Max')
    plt.scatter(times[equities.index(min_equity)], min_equity, color='red', label='Min')
    plt.scatter(times[-1], current_equity, color='orange', label='Current')
    plt.title("Vault Equity over last 24 hours")
    plt.xlabel("Time")
    plt.ylabel("Equity")
    plt.legend()
    plt.grid(True)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Start", callback_data="start")
        ]
    ])
    # Сохраняем во временный файл
    with tempfile.NamedTemporaryFile(suffix=".png") as tmp_file:
        plt.savefig(tmp_file.name)
        tmp_file.flush()  # убедимся, что всё записано

        await settings.telegram_bot.send_photo(chat_id=user_id,
                                               photo=FSInputFile(tmp_file.name, filename="vault_stats.png"),
                                               caption=text, reply_markup=keyboard)

    plt.close()