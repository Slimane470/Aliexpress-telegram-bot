# Telegram Deals Bot (AliExpress-ready)

A production-ready Telegram bot that posts discount deals. Uses a pluggable provider architecture so you can start with sample data and later switch to official AliExpress Affiliate API or another feed.

## Quick start

1) Create a bot and get the token from @BotFather

2) Copy `.env.example` to `.env` and fill values:

```
cp .env.example .env
```

3) Install dependencies and run in dev mode (polling):

```
python3 -m pip install -r requirements.txt
python3 -m src.bot
```

## Commands

- /start — Welcome and help
- /deals [category] [max_price] — Fetch top deals now (e.g., `/deals electronics 25`)
- /subscribe [category] [max_price] [interval_min] — Subscribe to periodic deals (e.g., `/subscribe electronics 25 120`)
- /unsubscribe — Stop receiving periodic deals
- /help — Show usage

## Provider architecture

The bot uses a provider interface located in `src/deals/providers`. Default is `sample` which reads from `data/sample_deals.json`.

Switch provider via env var `PROVIDER` (e.g., `sample`). You can add your own provider that hits AliExpress Affiliate API.

## Persistence

SQLite database file is created at `data/bot.sqlite3`.

## Docker

```
docker build -t deals-bot .
docker run --env-file .env deals-bot
```
