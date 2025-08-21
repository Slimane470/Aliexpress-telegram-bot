## AliExpress Telegram Bot

A Telegram bot that generates AliExpress affiliate links from product URLs and can also push curated deals to subscribers.

### Setup
1. Create `.env` from `.env.example` and fill:
   - `TELEGRAM_BOT_TOKEN`
   - `ALIEXPRESS_APP_KEY`, `ALIEXPRESS_APP_SECRET`, `ALIEXPRESS_TRACKING_ID`
   - Optional: `TARGET_CURRENCY`, `TARGET_LANGUAGE`, `QUERY_COUNTRY`, `DEALS_PUSH_INTERVAL_MINUTES`
2. Install dependencies (recommended: Docker):

#### Run with Docker
```bash
docker build -t aliexpress-telegram-bot .
docker run --rm -p 8080:8080 \
  -e TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN \
  -e ALIEXPRESS_APP_KEY=$ALIEXPRESS_APP_KEY \
  -e ALIEXPRESS_APP_SECRET=$ALIEXPRESS_APP_SECRET \
  -e ALIEXPRESS_TRACKING_ID=$ALIEXPRESS_TRACKING_ID \
  -e TARGET_CURRENCY=USD -e TARGET_LANGUAGE=en -e QUERY_COUNTRY=US \
  -e DEALS_PUSH_INTERVAL_MINUTES=360 \
  aliexpress-telegram-bot
```

### Commands
- /start: Welcome and usage
- /subscribe: Subscribe to periodic deals
- /unsubscribe: Unsubscribe from deals
- /deals: Show a few current deals now

Send any AliExpress product link and the bot will reply with affiliate links for multiple offers.

### Notes
- Deals are provided from `deals_provider.py` (static demo list). Replace with a real provider when ready.
- Subscribers are stored in `subscribers_store.py` using a JSON file (`subscribers.json`).
