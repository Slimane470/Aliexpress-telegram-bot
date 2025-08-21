## API Reference

Comprehensive reference for public modules, classes, and functions in this repository. Examples show typical usage patterns. All paths below assume Python 3.10+.

- iop SDK: request signing and HTTP client for AliExpress APIs
- app: Telegram bot logic, AliExpress helpers, caching, and handlers
- aliexpress_utils: lightweight HTML scraping fallbacks
- keep_alive: simple Flask server and self-ping utilities

### Conventions used
- Return annotations use Python typing. Optional values are noted as “may be None”.
- Examples are minimal and meant for scripts or REPL. For async examples, use `asyncio.run(...)`.

---

## Module: `iop`

Public surface is re-exported via `from iop.base import *`.

### Functions
- **sign(secret: str, api: str, parameters: dict[str, str]) -> str**: Returns the uppercase HMAC-SHA256 signature used by the AliExpress gateway.
  - Example:
```python
from iop import sign

sig = sign("your_app_secret", "aliexpress.affiliate.productdetail.get", {
    "app_key": "your_app_key",
    "timestamp": "1700000000000",
    "method": "aliexpress.affiliate.productdetail.get",
})
print(sig)
```

- **logApiError(appkey: str, sdkVersion: str, requestUrl: str, code: str, message: str) -> None**: Appends a log line to `~/logs/iopsdk.log.YYYY-MM-DD`.

### Classes
- **class IopRequest(api_pame: str, http_method: str = 'POST')**
  - Methods:
    - `add_api_param(key: str, value: str) -> None`
    - `add_file_param(key: str, value: Any) -> None`
    - `set_simplify() -> None` (sets JSON simplification)
    - `set_format(value: str) -> None` (e.g., `json`)

- **class IopResponse**
  - Attributes: `type`, `code`, `message`, `request_id`, `body` (parsed JSON dict)

- **class IopClient(server_url: str, app_key: str, app_secret: str, timeout: int = 30)**
  - Methods:
    - `execute(request: IopRequest, access_token: str | None = None) -> IopResponse`
  - Example: Product detail request
```python
from iop import IopClient, IopRequest

client = IopClient(
    "https://api-sg.aliexpress.com/sync",
    app_key="YOUR_KEY",
    app_secret="YOUR_SECRET",
)

req = IopRequest('aliexpress.affiliate.productdetail.get')
req.add_api_param('fields', 'product_main_image_url,target_sale_price,product_title,target_sale_price_currency')
req.add_api_param('product_ids', '1234567890')
req.add_api_param('target_currency', 'USD')
req.add_api_param('target_language', 'en')
req.add_api_param('tracking_id', 'your_tracking_id')
req.add_api_param('country', 'US')

resp = client.execute(req)
print(resp.body)
```

---

## Module: `app`

### Environment variables
- **TELEGRAM_BOT_TOKEN**: Telegram bot token from BotFather.
- **ALIEXPRESS_APP_KEY**, **ALIEXPRESS_APP_SECRET**: AliExpress Affiliate API credentials.
- **ALIEXPRESS_TRACKING_ID**: Your affiliate tracking ID.
- **TARGET_CURRENCY** (default `USD`), **TARGET_LANGUAGE** (default `en`), **QUERY_COUNTRY** (default `US`): Regional settings for product detail queries.

### Constants and configuration
- **ALIEXPRESS_API_URL**: `https://api-sg.aliexpress.com/sync`
- **QUERY_FIELDS**: default fields requested for product details
- **OFFER_PARAMS**: mapping of promotion types to query params used for building share URLs
- **OFFER_ORDER**: list driving offer ordering in messages

### Class
- **class CacheWithExpiry(expiry_seconds: int)**: Async-safe in-memory cache with TTL.
  - `await get(key) -> Any | None`
  - `await set(key, value) -> None`
  - `await clear_expired() -> int` (number of entries removed)

### URL and ID utilities
- **extract_product_id(url: str) -> str | None**: Extracts product ID, handles multiple URL patterns and `.aliexpress.us` domain.
- **extract_potential_aliexpress_urls(text: str) -> list[str]**: Finds AliExpress-standard and short URLs in text.
- **clean_aliexpress_url(url: str, product_id: str) -> str | None**: Rebuilds canonical product URL like `https://www.aliexpress.com/item/{id}.html`.
- **build_url_with_offer_params(base_url: str, params_to_add: dict[str, str]) -> str**: Adds promotion params and wraps in `https://star.aliexpress.com/share/share.htm?...&redirectUrl={base_url}`.
- **resolve_short_link(short_url: str, session: aiohttp.ClientSession) -> str | None**: Follows redirects; normalizes country and `.us` domain; caches results.

Examples:
```python
from app import extract_product_id, clean_aliexpress_url

url = 'https://www.aliexpress.com/item/1005001234567890.html?aff_fcid=...'
product_id = extract_product_id(url)
base = clean_aliexpress_url(url, product_id)
```

### AliExpress API wrappers (async)
- **await fetch_product_details_v2(product_id: str) -> dict | None**
  - Returns on success: `{ 'image_url': str | None, 'price': str | None, 'currency': str, 'title': str }`
  - Uses internal cache; falls back to parsing JSON string if needed; logs API errors.

- **await generate_affiliate_links_batch(target_urls: list[str]) -> dict[str, str | None]**
  - Returns a dict mapping each input URL to a promotion link or None.
  - Will prefix non-prefixed URLs with the `star.aliexpress.com/share/share.htm` wrapper automatically before the request.

Examples:
```python
import asyncio
from app import fetch_product_details_v2, generate_affiliate_links_batch

async def main():
    details = await fetch_product_details_v2('1005001234567890')
    print(details)

    links = await generate_affiliate_links_batch([
        'https://star.aliexpress.com/share/share.htm?platform=AE&businessType=ProductDetail&redirectUrl=https://www.aliexpress.com/item/1005001234567890.html'
    ])
    print(links)

asyncio.run(main())
```

### Telegram handlers
- **async def start(update, context) -> None**: Sends welcome and instructions.
- **async def handle_message(update, context) -> None**: Parses incoming text, extracts product URLs, resolves, and schedules processing.
- **async def process_product_telegram(product_id: str, base_url: str, update, context) -> None**: Fetches details, generates affiliate links for the configured offers, and sends a rich message with inline keyboard.
- **async def periodic_cache_cleanup(context) -> None**: JobQueue callback to remove expired cache entries.
- **def main() -> None**: Application bootstrap; sets handlers, jobs, and starts polling.

End-to-end example (manual trigger outside Telegram):
```python
import asyncio
from app import fetch_product_details_v2, build_url_with_offer_params, generate_affiliate_links_batch

async def demo(product_id: str):
    # Build a base URL and an offer URL
    base = f"https://www.aliexpress.com/item/{product_id}.html"
    coin_url = build_url_with_offer_params(base, {"sourceType": "620%26channel=coin", "afSmartRedirect": "y"})

    # Fetch details and generate an affiliate link
    details = await fetch_product_details_v2(product_id)
    links = await generate_affiliate_links_batch([coin_url])
    print(details, links[coin_url])

asyncio.run(demo('1005001234567890'))
```

---

## Module: `aliexpress_utils`

- **get_aliexpress_product_info(product_url: str) -> tuple[str | None, str | None]**: Best-effort HTML scrape for product title and main image.
  - Uses several fallbacks: DOM `h1`, `og:title`, keywords meta, and generic `h1`. Image via `.magnifier--image` or `og:image`.
  - Returns `(product_name, img_url)`; either may be `None` if not found.

- **get_product_details_by_id(product_id: str | int) -> tuple[str | None, str | None]**: Constructs `https://vi.aliexpress.com/item/{id}.html` then calls `get_aliexpress_product_info`.

Example:
```python
from aliexpress_utils import get_product_details_by_id

name, image = get_product_details_by_id('1005001234567890')
print(name, image)
```

---

## Module: `keep_alive`

- **keep_alive() -> None**: Starts a background Flask server on `0.0.0.0:8080`.
- **self_ping() -> None**: Infinite loop that pings the configured Render URL every 3 minutes.
- Helper:
  - `run() -> None`: Flask app runner used by `keep_alive`.

Example (standalone):
```python
# Running this module will start the Flask server and background pinger.
import keep_alive  # noqa: F401 (side effects start server and pinger)
```

---

## Notes and best practices
- Use the async cache-aware wrappers from `app` instead of directly calling the `iop` client from concurrent contexts.
- Batch link generation greatly reduces API calls and should be preferred when you have multiple URLs.
- Short links should be resolved via `resolve_short_link` to normalize country and subdomain differences before extracting product IDs.
- Respect AliExpress API rate limits and error messages logged by the `iop` SDK.

