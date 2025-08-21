from typing import List
from telegram import Update
from telegram.ext import ContextTypes

from .store import Store


def _parse_categories(arg_text: str) -> List[str]:
    raw = [c.strip().lower() for c in arg_text.split(",")]
    return [c for c in raw if c]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    store: Store = context.bot_data["store"]
    chat_id = update.effective_chat.id
    store.upsert_user(chat_id)
    await update.message.reply_text(
        "Welcome! You are subscribed to AliExpress deals.\n"
        "- Use /setcategories electronics,home to set your interests.\n"
        "- Use /setminprice 10 to filter by minimum price.\n"
        "- Use /categories to view your current settings."
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Commands:\n"
        "/start - Register and see welcome\n"
        "/setcategories <a,b,c> - Set categories\n"
        "/setminprice <amount> - Set minimum price\n"
        "/categories - Show current categories\n"
        "/deals - Fetch and show a few deals now"
    )


async def set_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    store: Store = context.bot_data["store"]
    chat_id = update.effective_chat.id
    args_text = (" ".join(context.args)).strip()
    if not args_text:
        await update.message.reply_text("Usage: /setcategories electronics,home")
        return
    cats = _parse_categories(args_text)
    if not cats:
        await update.message.reply_text("No valid categories provided.")
        return
    store.set_categories(chat_id, cats)
    await update.message.reply_text(f"Categories updated: {', '.join(cats)}")


async def set_min_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    store: Store = context.bot_data["store"]
    chat_id = update.effective_chat.id
    if not context.args:
        await update.message.reply_text("Usage: /setminprice 10")
        return
    try:
        amount = float(context.args[0])
    except ValueError:
        await update.message.reply_text("Please provide a numeric amount, e.g. /setminprice 10")
        return
    store.set_min_price(chat_id, amount)
    await update.message.reply_text(f"Minimum price set to {amount:.2f}")


async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    store: Store = context.bot_data["store"]
    chat_id = update.effective_chat.id
    user = store.get_user(chat_id)
    if not user:
        await update.message.reply_text("You are not registered. Use /start first.")
        return
    cats = user["categories"]
    min_price = user["min_price"]
    cats_text = ", ".join(cats) if cats else "(none)"
    await update.message.reply_text(f"Categories: {cats_text}\nMin price: {min_price:.2f}")