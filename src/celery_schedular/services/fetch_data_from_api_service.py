import httpx

from DB.managers.vaults_manager import VaultsManager
from DB.sqlalchemy_database_manager import async_session
from core.custom_logs import log


async def async_fetch_data_from_api():
    """Asynchronous task to fetch data from an API."""
    log.info("[TASK] Fetching data from an API...")
    URL = "https://starknet.app.extended.exchange/api/v1/vault/public/summary"

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(URL)
        response.raise_for_status()
        data = response.json()
        log.info(f"[TASK] Data fetched from API: {data}")
    async with async_session() as session:
        vault_manager = VaultsManager(session)
        data=data.get("data")
        equity=data.get("equity")
        wallet_balance=data.get("walletBalance")
        last_30_days_apr=data.get("last30dApr")
        exposure=data.get("exposure")
        numberOfDepositors=data.get("numberOfDepositors")
        age_days=data.get("ageDays")
        profit_share=data.get("profitShare")
        if vault_manager is None or equity is None or wallet_balance is None or last_30_days_apr is None or exposure is None or numberOfDepositors is None or age_days is None or profit_share is None:
            return None

        await vault_manager.upload_vaults_data(equity=equity,
                                 wallet_balance=wallet_balance,
                                 last_30_days_apr=last_30_days_apr,
                                 exposure=exposure,
                                 numberOfDepositors=numberOfDepositors,
                                 age_days=age_days,
                                 profit_share=profit_share)
        return data