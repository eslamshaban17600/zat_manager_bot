import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    OWNER_USER_ID: int = int(os.getenv("OWNER_USER_ID", "0"))
    DB_URL: str = os.getenv("DB_URL", "sqlite+aiosqlite:///./data/zat_bot.db")
    TIMEZONE: str = os.getenv("TIMEZONE", "Africa/Cairo")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()