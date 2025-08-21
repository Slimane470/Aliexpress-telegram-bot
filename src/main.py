import logging
from typing import List

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from .config import settings
from .store import Store
from . import handlers as h
from .deals_provider import fetch_top_deals, filter_deals


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


async def send_periodic_deals(context: ContextTypes.DEFAULT_TYPE) -> None:
    store: Store = context.bot_data["store"]
    all_deals = fetch_top_deals(limit=20)
    users = store.get_all_users()
    for user in users:
        try:
            filtered = filter_deals(
                deals=all_deals,
                categories=user["categories"],
                min_price=user["min_price"],
                limit=3,
            )
            if not filtered:
                continue
            lines = [f"{d.title} — ${d.price:.2f}\n{d.url}" for d in filtered]
            text = "\n\n".join(lines)
            await context.bot.send_message(chat_id=user["chat_id"], text=text)
        except Exception as exc:
            logger.exception("Failed sending deals to %s: %s", user["chat_id"], exc)


async def deals_now(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    store: Store = context.bot_data["store"]
    chat_id = update.effective_chat.id
    user = store.get_user(chat_id)
    if not user:
        await update.message.reply_text("You are not registered. Use /start first.")
        return
    all_deals = fetch_top_deals(limit=20)
    filtered = filter_deals(
        deals=all_deals,
        categories=user["categories"],
        min_price=user["min_price"],
        limit=5,
    )
    if not filtered:
        await update.message.reply_text("No deals match your preferences right now.")
        return
    lines = [f"{d.title} — ${d.price:.2f}\n{d.url}" for d in filtered]
    await update.message.reply_text("\n\n".join(lines))


def main() -> None:
    if not settings.bot_token:
        raise RuntimeError("BOT_TOKEN is not set. Provide it via environment or .env file.")

    store = Store(settings.db_path)

    app = (
        ApplicationBuilder()
        .token(settings.bot_token)
        .post_init(lambda app: app.bot_data.__setitem__("store", store))
        .build()
    )

    app.add_handler(CommandHandler("start", h.start))
    app.add_handler(CommandHandler("help", h.help_cmd))
    app.add_handler(CommandHandler("setcategories", h.set_categories))
    app.add_handler(CommandHandler("setminprice", h.set_min_price))
    app.add_handler(CommandHandler("categories", h.show_categories))
    app.add_handler(CommandHandler("deals", deals_now))

    job_queue = app.job_queue
    job_queue.run_repeating(send_periodic_deals, interval=settings.fetch_interval_minutes * 60, first=30)

    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()