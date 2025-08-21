import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    bot_token: str = os.getenv("BOT_TOKEN", "")
    fetch_interval_minutes: int = int(os.getenv("FETCH_INTERVAL_MINUTES", "360"))
    db_path: str = os.getenv("DB_PATH", "/workspace/data/bot.db")


settings = Settings()