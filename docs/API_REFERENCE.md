## API Reference

Comprehensive reference for public modules, classes, and functions in this project. Examples are provided where applicable.

### Conventions
- Coroutines are annotated with async and must be awaited.
- Types are provided for clarity; some functions may not enforce runtime types.

---

## Module: `app.py`

### Constants and Configuration
- `ALIEXPRESS_API_URL: str` – Base URL for the AliExpress API.
- `QUERY_FIELDS: str` – Product fields requested from `aliexpress.affiliate.productdetail.get`.
- `TARGET_CURRENCY: str` – Target currency for API responses (via `.env`).
- `TARGET_LANGUAGE: str` – Target language for API responses (via `.env`).
- `QUERY_COUNTRY: str` – Country used for product detail queries (via `.env`).
- `ALIEXPRESS_TRACKING_ID: str` – Affiliate tracking ID (via `.env`).
- `CACHE_EXPIRY_DAYS: int` – Days to retain cache items (default 1).

### Class: `CacheWithExpiry`
Thread-safe (async) in-memory cache with time-based expiry.

Methods:
- `async def get(key: str) -> Any | None`
  - Returns a cached value if present and not expired, else `None`.
- `async def set(key: str, value: Any) -> None`
  - Stores `value` under `key` with current timestamp.
- `async def clear_expired() -> int`
  - Removes expired items and returns the number removed.

Example:
```python
cache = CacheWithExpiry(60)
await cache.set("foo", {"bar": 1})
value = await cache.get("foo")  # {"bar": 1}
removed = await cache.clear_expired()
```

### Function: `async def resolve_short_link(short_url: str, session: aiohttp.ClientSession) -> str | None`
Follows redirects for AliExpress short links (`s.click`, `a.aliexpress`) and normalizes domain/country parameters, returning the final URL or `None`.

Example:
```python
async with aiohttp.ClientSession() as session:
    final_url = await resolve_short_link("https://s.click.aliexpress.com/e/xxxx", session)
```

### Function: `def extract_product_id(url: str) -> str | None`
Extracts a numeric AliExpress product ID from product URLs (handles `.us` domain and alternative patterns). Returns `None` if not found.

Example:
```python
pid = extract_product_id("https://www.aliexpress.com/item/1234567890.html")
# "1234567890"
```

### Function: `def extract_potential_aliexpress_urls(text: str) -> list[str]`
Finds potential AliExpress URLs (standard and short) within arbitrary text.

### Function: `def clean_aliexpress_url(url: str, product_id: str) -> str | None`
Rebuilds a clean product URL using the extracted `product_id` while preserving scheme and domain. Returns `None` on parse failures.

Example:
```python
clean = clean_aliexpress_url(
    "https://www.aliexpress.com/item/1234567890.html?spm=xxx",
    "1234567890",
)
# "https://www.aliexpress.com/item/1234567890.html"
```

### Function: `def build_url_with_offer_params(base_url: str, params_to_add: dict[str, str]) -> str`
Adds offer parameters to `base_url`, normalizes country subdomains, and wraps the URL with `star.aliexpress.com/share/share.htm` redirect.

Example:
```python
offer_url = build_url_with_offer_params(
    "https://www.aliexpress.com/item/1234567890.html",
    {"sourceType": "562", "channel": "sd"},
)
```

### Function: `async def periodic_cache_cleanup(context) -> None`
JobQueue callback that purges expired items from caches and logs stats.

### Function: `async def fetch_product_details_v2(product_id: str) -> dict | None`
Fetches product details using `aliexpress.affiliate.productdetail.get`, with async caching and error handling.

Returns (on success):
```python
{
  "image_url": str | None,
  "price": str | None,
  "currency": str,
  "title": str
}
```

Example:
```python
details = await fetch_product_details_v2("1234567890")
if details:
    print(details["title"], details["price"], details["currency"]) 
```

### Function: `async def generate_affiliate_links_batch(target_urls: list[str]) -> dict[str, str | None]`
Generates affiliate links for a list of target URLs via a single AliExpress API call. Cached results are reused.

Example:
```python
targets = [
  "https://star.aliexpress.com/share/share.htm?platform=AE&businessType=ProductDetail&redirectUrl=https://www.aliexpress.com/item/123.html",
  "https://star.aliexpress.com/share/share.htm?platform=AE&businessType=ProductDetail&redirectUrl=https://www.aliexpress.com/item/456.html",
]
links = await generate_affiliate_links_batch(targets)
```

### Function: `async def start(update, context) -> None`
Telegram `/start` command handler. Sends a welcome/how-to message.

### Function: `async def process_product_telegram(product_id: str, base_url: str, update, context) -> None`
Internal helper that fetches product details, builds offer URLs, generates affiliate links, and replies to the chat with formatted content and inline buttons.

### Function: `async def handle_message(update, context) -> None`
Main message handler for messages containing AliExpress links. Extracts/normalizes links, resolves short links, deduplicates products, and dispatches processing tasks.

### Function: `def main() -> None`
Bootstraps the Telegram application, registers handlers, schedules periodic jobs, and starts polling.

---

## Module: `aliexpress_utils.py`

### Function: `def get_aliexpress_product_info(product_url: str) -> tuple[str | None, str | None]`
Scrapes product name and image URL from a given AliExpress product page, using `requests` and `BeautifulSoup` with several fallbacks.

Returns `(product_name, image_url)` where either value may be `None`.

Example:
```python
name, image = get_aliexpress_product_info("https://www.aliexpress.com/item/1234567890.html")
```

### Function: `def get_product_details_by_id(product_id: str | int) -> tuple[str | None, str | None]`
Builds the canonical product URL from `product_id` and calls `get_aliexpress_product_info`.

Example:
```python
name, image = get_product_details_by_id(1234567890)
```

---

## Module: `iop/base.py`

AliExpress/Alibaba IOP SDK client and request/response helpers used to invoke official API methods.

### Function: `def sign(secret: str, api: str, parameters: dict[str, Any]) -> str`
Generates an uppercase SHA-256 HMAC signature over sorted parameters; used internally by `IopClient`.

### Function: `def logApiError(appkey: str, sdkVersion: str, requestUrl: str, code: str, message: str) -> None`
Writes a single-line log record to `~/logs/iopsdk.log.YYYY-MM-DD` for diagnostics.

### Class: `IopRequest`
Represents an API request to the IOP gateway.

Constructor:
- `IopRequest(api_name: str, http_method: str = 'POST')`

Methods:
- `add_api_param(key: str, value: Any) -> None`
- `add_file_param(key: str, value: Any) -> None`
- `set_simplify() -> None`
- `set_format(value: str) -> None`  # e.g., "json"

### Class: `IopResponse`
Holds parsed response metadata and `body` (dict) from the gateway.

Attributes: `type`, `code`, `message`, `request_id`, `body`.

### Class: `IopClient`
Low-level HTTP client for executing IOP requests.

Constructor:
- `IopClient(server_url: str, app_key: str, app_secret: str, timeout: int = 30)`

Method:
- `execute(request: IopRequest, access_token: str | None = None) -> IopResponse`

Example:
```python
client = IopClient(ALIEXPRESS_API_URL, ALIEXPRESS_APP_KEY, ALIEXPRESS_APP_SECRET)
req = IopRequest('aliexpress.affiliate.productdetail.get')
req.add_api_param('fields', 'product_main_image_url,target_sale_price,product_title,target_sale_price_currency')
req.add_api_param('product_ids', '1234567890')
req.add_api_param('target_currency', 'USD')
req.add_api_param('target_language', 'en')
req.add_api_param('tracking_id', 'yourTrackingId')
req.add_api_param('country', 'US')
resp = client.execute(req)
print(resp.body)
```

---

## Module: `keep_alive.py`

Simple Flask-based keep-alive ping service.

### HTTP Endpoint: `GET /`
Returns a plain text body "?". Useful for uptime monitors.

### Function: `def keep_alive() -> None`
Starts the Flask app in a background thread bound to `0.0.0.0:8080`.

### Function: `def self_ping() -> None`
Periodically pings the hosted URL to keep the service awake.

---

## Telegram Interface

- `/start` – Sends a welcome/how-to message.
- Message with AliExpress URL – Triggers product parsing, details lookup, and generation of multiple affiliate links with inline buttons.

---

## End-to-End Example (Message Flow)
```text
User sends: "Check this out https://www.aliexpress.com/item/1234567890.html"
-> Bot extracts/normalizes URL and product ID
-> Bot fetches product details (API first, scrape fallback)
-> Bot generates affiliate links for configured offers (batch)
-> Bot replies with image (if available), price, and offer buttons
```

