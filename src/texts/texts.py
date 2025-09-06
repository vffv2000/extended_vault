from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

SET_LIMIT_BTN_TEXT = "💰 Set Target Amount"
STATS_BTN_TEXT = "📊 Vault Stats"
START_BTN_TEXT = "🚀 Start Monitoring"
CLICK_BTN_TEXT = "👆 CLICK"



INPUT_NUMBER_TEXT = """
💰 Please enter a new target amount (number).
⚠️ It must be greater than 0 and less than 100,000.
"""
INPUT_NUMBER_ERROR = "❌ Please enter a valid number."
INPUT_NUMBER_ERROR_2 = "⚠️ Amount must be greater than 0 and less than 100,000."

HELP_TEXT = """
🤖 Dex Extended Vault Monitor Bot

This bot helps you track the available space in Dex Extended vaults. 
Set your target amount and get notified as soon as there is enough space to deposit.

Commands:
/start - start the bot
/stats - get stats about vaults (max, min, current equity)
/help - show this help message
"""

async def build_start_text(status:bool,limit:float):
    status_str = "ON" if status else "OFF"
    if limit is None:
        limit_str = "not set"
    else:
        limit_str = f"{limit:.0f}"


    text = f"""
🤖 This bot helps you track Dex Extended vaults.  
You have three main buttons:

🔔 Turn ON/Turn OFF notifications  
Current status: <b>{status_str}</b>

⚙️ Change your limit  
Current limit: <b>{limit_str}</b>

📊 View vault filling statistics  
"""

    return text

async def build_notification_text(limit:float, equity:float,):
    text = f"""
⚠️⚠️⚠️ ALERT ⚠️⚠️⚠️

Your target amount <b>{limit}</b> can now be added to the vault! 🎉
Current equity: <b>{equity}</b>

⚠️⚠️⚠️ ALERT ⚠️⚠️⚠️
"""
    return text

async def built_stats_text(max_equity,min_equity,current_equity):
    text = f"""
<b>📊 Vault statistics (last 24h)</b>
🔺 Max equity: <code>{max_equity:.0f}</code>
🔻 Min equity: <code>{min_equity:.0f}</code>
⚖️ Current equity: <code>{current_equity:.0f}</code>

📈 A chart showing vault equity changes over the last 24 hours is also attached.
    """


    return text

async def build_start_keyboard(status: bool) -> InlineKeyboardMarkup:
    if status:
        btn_text = "🔴 Turn off notifications"
    else:
        btn_text = "🟢 Turn on notifications"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=btn_text, callback_data="toggle_notify"),
        ],
        [
            InlineKeyboardButton(text=SET_LIMIT_BTN_TEXT, callback_data="set_limit")
        ],
        [
            InlineKeyboardButton(text=STATS_BTN_TEXT, callback_data="stats")
        ]
    ])
    return keyboard

async def build_help_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=START_BTN_TEXT, callback_data="start"),
        ],
        [
            InlineKeyboardButton(text=STATS_BTN_TEXT, callback_data="stats")
        ]
    ])
    return keyboard

async def build_stats_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=START_BTN_TEXT, callback_data="start")
        ]
    ])
    return keyboard

async def build_notification_keyboard() -> InlineKeyboardMarkup:
    url = "https://app.extended.exchange/vault"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=CLICK_BTN_TEXT, url=url),
        ]
    ])
    return keyboard