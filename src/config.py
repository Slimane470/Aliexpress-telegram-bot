import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


def _get_env_list(name: str) -> list[int]:
    value = os.getenv(name, "").strip()
    if not value:
        return []
    items = []
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            items.append(int(part))
        except ValueError:
            continue
    return items


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    admin_user_ids: list[int]
    provider: str
    sample_deals_json: str
    default_subscription_interval_min: int
    database_path: str
    timezone: str


def get_settings() -> Settings:
    return Settings(
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", "").strip(),
        admin_user_ids=_get_env_list("ADMIN_USER_IDS"),
        provider=os.getenv("PROVIDER", "sample").strip() or "sample",
        sample_deals_json=os.getenv("SAMPLE_DEALS_JSON", "data/sample_deals.json"),
        default_subscription_interval_min=int(os.getenv("DEFAULT_SUBSCRIPTION_INTERVAL_MIN", "180")),
        database_path=os.getenv("DATABASE_PATH", "data/bot.sqlite3"),
        timezone=os.getenv("TZ", "UTC"),
    )