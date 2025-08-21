## Usage Guide

This guide explains how to configure, run, and use the AliExpress Affiliate Telegram Bot, and how to use its modules programmatically.

### Quick Start
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Create a `.env` file with your credentials:
```dotenv
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
ALIEXPRESS_APP_KEY=YOUR_ALIEXPRESS_APP_KEY
ALIEXPRESS_APP_SECRET=YOUR_ALIEXPRESS_APP_SECRET
ALIEXPRESS_TRACKING_ID=YOUR_TRACKING_ID
TARGET_CURRENCY=USD
TARGET_LANGUAGE=en
QUERY_COUNTRY=US
```
3. Run the bot:
```bash
python app.py
```

### Using the Bot on Telegram
- Send `/start` to see a quick how-to.
- Send a message containing one or more AliExpress product links. The bot will:
  - Extract and normalize product URLs
  - Fetch product details (title, price, image)
  - Generate multiple affiliate links (Coin, Super Deals, Limited Offers, Big Save)
  - Reply with a formatted message and inline buttons

### Programmatic Usage (Python)
You can reuse the internal functions in your own scripts.

Fetch product details:
```python
import asyncio
from app import fetch_product_details_v2

async def main():
    details = await fetch_product_details_v2("1234567890")
    print(details)

asyncio.run(main())
```

Generate affiliate links for offer pages:
```python
import asyncio
from app import build_url_with_offer_params, generate_affiliate_links_batch

async def main():
    base = "https://www.aliexpress.com/item/1234567890.html"
    targets = [
        build_url_with_offer_params(base, {"sourceType": "562", "channel": "sd"}),
        build_url_with_offer_params(base, {"sourceType": "561", "channel": "limitedoffers"}),
    ]
    links = await generate_affiliate_links_batch(targets)
    print(links)

asyncio.run(main())
```

Extract product IDs and clean URLs:
```python
from app import extract_product_id, clean_aliexpress_url

url = "https://www.aliexpress.com/item/1234567890.html?spm=foo"
pid = extract_product_id(url)
clean = clean_aliexpress_url(url, pid)
print(pid, clean)
```

Resolve short links:
```python
import asyncio, aiohttp
from app import resolve_short_link

async def main():
    async with aiohttp.ClientSession() as session:
        final_url = await resolve_short_link("https://s.click.aliexpress.com/e/xxxx", session)
        print(final_url)

asyncio.run(main())
```

### Customizing Offers
Offers are defined in `app.py`:
- `OFFER_PARAMS` maps offer keys to display names and URL parameters.
- `OFFER_ORDER` controls display order.

Add a new offer (example):
```python
OFFER_PARAMS["flash"] = {"name": "⚡ Flash Deals", "params": {"sourceType": "590", "channel": "flash"}}
OFFER_ORDER.append("flash")
```

### Caching
- Uses an async in-memory cache (`CacheWithExpiry`).
- Default expiry is `CACHE_EXPIRY_DAYS = 1` for both product details and generated links.
- A periodic job cleans expired items daily via `JobQueue`.

### Deployment Notes
- The optional `keep_alive.py` exposes a simple Flask endpoint (`/`) and a self-ping loop suitable for platforms that sleep inactive apps.
- Ensure required ports and environment variables are configured in your hosting environment (e.g., Docker, Render, CapRover).

### Troubleshooting
- "Missing required environment variables" – Verify `.env` values and that your environment loads them.
- "No AliExpress links found" – Ensure the message contains a valid AliExpress product URL.
- No image/price – The API may not return details; the bot falls back to scraping for title/image.
- No affiliate links – API may fail or reject some URLs; review logs and your `ALIEXPRESS_TRACKING_ID`.

### Security
- Never commit real tokens/keys. Use `.env` and secret managers.
- Rotate credentials if you suspect exposure.

### References
- See the full API surface in the [API Reference](API_REFERENCE.md).

