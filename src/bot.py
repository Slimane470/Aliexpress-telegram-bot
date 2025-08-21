from __future__ import annotations

import logging
import os
from typing import Optional, Sequence

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from .config import get_settings
from .db import Database
from .deals.fetcher import fetch_deals
from .utils.text import format_deals_md


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("deals-bot")


def _parse_float(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except Exception:
        return None


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat = update.effective_chat
    settings = get_settings()
    db: Database = context.application.bot_data["db"]

    db.upsert_user(
        chat_id=chat.id,
        username=(user.username if user else None),
        first_name=(user.first_name if user else None),
        last_name=(user.last_name if user else None),
        language_code=(user.language_code if user else None),
    )

    text = (
        "Welcome! I will send you great deals.\n\n"
        "Commands:\n"
        "- /deals [category] [max_price]\n"
        "- /subscribe [category] [max_price] [interval_min]\n"
        "- /unsubscribe\n"
        "- /help\n"
    )
    await update.message.reply_text(text)


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Usage:\n"
        "- /deals [category] [max_price]\n"
        "- /subscribe [category] [max_price] [interval_min]\n"
        "- /unsubscribe\n"
    )


async def cmd_deals(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    category = args[0] if len(args) >= 1 else None
    max_price = _parse_float(args[1]) if len(args) >= 2 else None

    deals = fetch_deals(category=category, max_price=max_price, limit=10)

    if not deals:
        await update.message.reply_text("No deals found right now. Try again later or adjust filters.")
        return

    await update.message.reply_text(
        format_deals_md(deals),
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_web_page_preview=False,
    )


async def _send_deals_to_chat(context: ContextTypes.DEFAULT_TYPE) -> None:
    job_data = context.job.data or {}
    chat_id: int = job_data.get("chat_id")
    category: Optional[str] = job_data.get("category")
    max_price: Optional[float] = job_data.get("max_price")

    db: Database = context.application.bot_data["db"]
    deals = fetch_deals(category=category, max_price=max_price, limit=10)
    if not deals:
        return

    # Avoid duplicates per chat
    unique_deals = []
    for d in deals:
        if not db.was_deal_delivered(chat_id, d.id):
            unique_deals.append(d)
            db.mark_deal_delivered(chat_id, d.id)

    if not unique_deals:
        return

    await context.bot.send_message(
        chat_id=chat_id,
        text=format_deals_md(unique_deals),
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_web_page_preview=False,
    )


async def cmd_subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings = get_settings()
    args = context.args
    category = args[0] if len(args) >= 1 else None
    max_price = _parse_float(args[1]) if len(args) >= 2 else None
    interval_min = int(args[2]) if len(args) >= 3 else settings.default_subscription_interval_min

    chat_id = update.effective_chat.id
    db: Database = context.application.bot_data["db"]

    db.upsert_subscription(chat_id=chat_id, category=category, max_price=max_price, interval_min=interval_min)

    # Cancel prior job if exists
    job_name = f"sub_{chat_id}"
    for job in context.job_queue.get_jobs_by_name(job_name):
        job.schedule_removal()

    # Schedule new job
    context.job_queue.run_repeating(
        _send_deals_to_chat,
        interval=interval_min * 60,
        first=0,
        name=job_name,
        data={"chat_id": chat_id, "category": category, "max_price": max_price},
    )

    await update.message.reply_text(
        f"Subscribed! Category={category or 'any'}, Max Price={max_price or 'any'}, Interval={interval_min} min"
    )


async def cmd_unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    db: Database = context.application.bot_data["db"]

    db.delete_subscription(chat_id)

    job_name = f"sub_{chat_id}"
    removed = False
    for job in context.job_queue.get_jobs_by_name(job_name):
        job.schedule_removal()
        removed = True

    await update.message.reply_text("Unsubscribed." if removed else "You were not subscribed.")


async def cmd_ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("pong")


def _restore_jobs_from_db(app: Application) -> None:
    db: Database = app.bot_data["db"]
    for row in db.list_subscriptions():
        chat_id = int(row["chat_id"]) if row["chat_id"] is not None else None
        category = row["category"]
        max_price = float(row["max_price"]) if row["max_price"] is not None else None
        interval_min = int(row["interval_min"]) if row["interval_min"] is not None else 60
        if chat_id is None:
            continue
        job_name = f"sub_{chat_id}"
        app.job_queue.run_repeating(
            _send_deals_to_chat,
            interval=interval_min * 60,
            first=5,
            name=job_name,
            data={"chat_id": chat_id, "category": category, "max_price": max_price},
        )
        logger.info("Restored subscription for chat %s", chat_id)


def main() -> None:
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is required. Put it in .env or env vars.")

    db = Database(settings.database_path)

    application: Application = ApplicationBuilder().token(settings.telegram_bot_token).build()
    application.bot_data["db"] = db

    application.add_handler(CommandHandler("start", cmd_start))
    application.add_handler(CommandHandler("help", cmd_help))
    application.add_handler(CommandHandler("deals", cmd_deals))
    application.add_handler(CommandHandler("subscribe", cmd_subscribe))
    application.add_handler(CommandHandler("unsubscribe", cmd_unsubscribe))
    application.add_handler(CommandHandler("ping", cmd_ping))

    _restore_jobs_from_db(application)

    logger.info("Bot started (polling)")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()