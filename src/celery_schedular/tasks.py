"""Celery tasks for periodic operations."""
import asyncio
import time

from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from celery import shared_task

from DB.managers.users_manager import UserManager
from DB.managers.vaults_manager import VaultsManager
from DB.sqlalchemy_database_manager import async_session
from celery_schedular.services.fetch_data_from_api_service import async_fetch_data_from_api
from core.config import settings
from core.custom_logs import log
from texts.texts import build_notification_keyboard, build_notification_text


@shared_task
def print_unix():
    """Celery task to print the current UNIX time."""
    ts = int(time.time())
    log.info(f"[TASK] Current UNIX time: {ts}")

@shared_task
def fetch_data_from_api():
    """Celery task to fetch data from an API."""
    log.info("[TASK] Fetching data from an API...")
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(async_fetch_data_from_api())
    return result


@shared_task
def send_alert():
    """Celery task to send an alert."""
    log.info("[TASK] Sending an alert...")
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(async_send_alert())
    return result

async def async_send_alert():
    log.info("[TASK] Sending an alert...")
    async with async_session() as session:
        vault_manager = VaultsManager(session)
        vault_data = await vault_manager.get_last_vault()
        equity=vault_data.equity
        current_free_space = 20000000-float(equity)
        async with async_session() as session:
            user_manager = UserManager(session)
            users= await user_manager.get_and_update_users_for_notification(value=current_free_space)
            log.info(f"[TASK] Users for notification: {len(users)}")
        for user in users:
            log.info(f"[TASK] Sending alert to user {user.telegram_id}")
            message =await build_notification_text(limit=user.limit,
                                                   equity=equity)


            await settings.telegram_bot.send_message(user.telegram_id, message,
                                                     reply_markup=await build_notification_keyboard(),
                                                     parse_mode=ParseMode.HTML)