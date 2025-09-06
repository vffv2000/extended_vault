from aiogram import Bot
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    #Settings


    # Database settings
    db_host: str = Field(..., description="Database host", env="DB_HOST")
    db_name: str = Field(..., description="Database name", env="DB_NAME")
    db_port: str = Field(..., description="Database port", env="DB_PORT")
    db_user: str = Field(..., description="Database user", env="DB_USER")
    db_password: str = Field(..., description="Database password", env="DB_PASSWORD")

    telegram_bot_api_key: str = Field(..., description="Telegram Bot API Key", env="TELEGRAM_BOT_API_KEY")

    rabbitmq_admin_login:str = Field(...,description="Login for RabbitMQ admin panel",env="RABBITMQ_ADMIN_LOGIN")
    rabbitmq_admin_pass:str = Field(...,description="Password for RabbitMQ admin panel",env="RABBITMQ_ADMIN_PASS")

    class Config:
        """Configuration for Pydantic settings."""

        env_file = ".env"

    @property
    def telegram_bot(self) -> Bot:
        """Generate the Telegram bot instance."""
        return Bot(token=self.telegram_bot_api_key)

    @property
    def broker_for_rabbitmq(self) -> str:
        """Generate the broker URL for RabbitMQ."""
        return f"amqp://{self.rabbitmq_admin_login}:{self.rabbitmq_admin_pass}@rabbitmq:5672//"

    @property
    def get_database_connection_string(self) -> str:
        """Generate the database connection string for asyncpg."""
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def get_sync_database_connection_string(self) -> str:
        """Generate the database connection string for psycopg."""
        return f"postgresql://{self.db_user}:{self.db_password}@localhost:{self.db_port}/{self.db_name}"

settings = Settings()