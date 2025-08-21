# AliExpress Telegram Bot - API Reference

## Overview

This AliExpress Telegram Bot is a comprehensive solution for processing AliExpress product links and generating affiliate links with various discount offers. The bot integrates with the AliExpress API, provides web scraping fallbacks, and includes caching mechanisms for optimal performance.

## Table of Contents

1. [Main Application Module (`app.py`)](#main-application-module-apppy)
2. [AliExpress Utilities (`aliexpress_utils.py`)](#aliexpress-utilities-aliexpress_utilspy)
3. [IOP SDK Module (`iop/`)](#iop-sdk-module-iop)
4. [Keep Alive Module (`keep_alive.py`)](#keep-alive-module-keep_alivepy)
5. [Configuration](#configuration)
6. [Usage Examples](#usage-examples)

---

## Main Application Module (`app.py`)

The main application module contains the core Telegram bot functionality, API integrations, and business logic.

### Classes

#### `CacheWithExpiry`

A thread-safe asynchronous cache implementation with automatic expiry functionality.

**Constructor:**
```python
CacheWithExpiry(expiry_seconds: int)
```

**Parameters:**
- `expiry_seconds` (int): The number of seconds after which cached items expire

**Methods:**

##### `async get(key: str) -> Any | None`
Retrieves an item from the cache if it exists and hasn't expired.

**Parameters:**
- `key` (str): The cache key to retrieve

**Returns:**
- The cached value if found and not expired, otherwise `None`

**Example:**
```python
cache = CacheWithExpiry(3600)  # 1 hour expiry
value = await cache.get("product_123")
```

##### `async set(key: str, value: Any) -> None`
Stores an item in the cache with the current timestamp.

**Parameters:**
- `key` (str): The cache key
- `value` (Any): The value to cache

**Example:**
```python
await cache.set("product_123", {"title": "Product Name", "price": 29.99})
```

##### `async clear_expired() -> int`
Removes all expired items from the cache.

**Returns:**
- `int`: The number of expired items removed

**Example:**
```python
removed_count = await cache.clear_expired()
print(f"Removed {removed_count} expired items")
```

### Core Functions

#### `async resolve_short_link(short_url: str, session: aiohttp.ClientSession) -> str | None`

Resolves shortened URLs by following redirects to find the final destination URL.

**Parameters:**
- `short_url` (str): The shortened URL to resolve
- `session` (aiohttp.ClientSession): HTTP session for making requests

**Returns:**
- `str | None`: The final resolved URL, or `None` if resolution failed

**Features:**
- Automatic domain conversion from `.aliexpress.us` to `.aliexpress.com`
- Country parameter normalization
- Caching of resolved URLs
- Timeout handling (10 seconds)

**Example:**
```python
async with aiohttp.ClientSession() as session:
    final_url = await resolve_short_link("https://s.click.aliexpress.com/e/_abc123", session)
    if final_url:
        print(f"Resolved to: {final_url}")
```

#### `extract_product_id(url: str) -> str | None`

Extracts the AliExpress product ID from various URL formats.

**Parameters:**
- `url` (str): The AliExpress product URL

**Returns:**
- `str | None`: The extracted product ID, or `None` if not found

**Supported URL Formats:**
- `https://www.aliexpress.com/item/123456789.html`
- `https://vi.aliexpress.com/item/123456789.html`
- `https://www.aliexpress.us/item/123456789.html`
- URLs with additional parameters

**Example:**
```python
product_id = extract_product_id("https://www.aliexpress.com/item/1234567890.html")
print(f"Product ID: {product_id}")  # Output: 1234567890
```

#### `extract_potential_aliexpress_urls(text: str) -> list[str]`

Extracts potential AliExpress URLs from text using regular expressions.

**Parameters:**
- `text` (str): The text to search for URLs

**Returns:**
- `list[str]`: A list of found AliExpress URLs

**Supported Patterns:**
- Standard AliExpress domains
- Shortened click URLs
- Various subdomains and country-specific domains

**Example:**
```python
text = "Check out this product: https://www.aliexpress.com/item/123.html and this one: https://s.click.aliexpress.com/e/_abc"
urls = extract_potential_aliexpress_urls(text)
print(urls)  # ['https://www.aliexpress.com/item/123.html', 'https://s.click.aliexpress.com/e/_abc']
```

#### `clean_aliexpress_url(url: str, product_id: str) -> str | None`

Cleans and standardizes AliExpress URLs by removing unnecessary parameters.

**Parameters:**
- `url` (str): The original URL to clean
- `product_id` (str): The product ID to include in the cleaned URL

**Returns:**
- `str | None`: The cleaned URL, or `None` if cleaning failed

**Example:**
```python
clean_url = clean_aliexpress_url("https://www.aliexpress.com/item/123.html?param1=value1&param2=value2", "123")
print(clean_url)  # https://www.aliexpress.com/item/123.html
```

#### `build_url_with_offer_params(base_url: str, params_to_add: dict) -> str | None`

Builds a URL with additional offer parameters for affiliate links.

**Parameters:**
- `base_url` (str): The base AliExpress product URL
- `params_to_add` (dict): Dictionary of parameters to add to the URL

**Returns:**
- `str | None`: The URL with added parameters, or `None` if failed

**Example:**
```python
params = {"coin": "1", "super": "1"}
offer_url = build_url_with_offer_params("https://www.aliexpress.com/item/123.html", params)
```

#### `async fetch_product_details_v2(product_id: str) -> dict | None`

Fetches product details from the AliExpress API with caching support.

**Parameters:**
- `product_id` (str): The AliExpress product ID

**Returns:**
- `dict | None`: Product details dictionary or `None` if failed

**Response Structure:**
```python
{
    "image_url": "https://...",
    "price": "29.99",
    "currency": "USD",
    "title": "Product Title"
}
```

**Features:**
- Automatic caching with configurable expiry
- Thread pool execution for non-blocking API calls
- Comprehensive error handling
- Detailed logging

**Example:**
```python
details = await fetch_product_details_v2("1234567890")
if details:
    print(f"Title: {details['title']}")
    print(f"Price: {details['price']} {details['currency']}")
```

#### `async generate_affiliate_links_batch(target_urls: list[str]) -> dict[str, str | None]`

Generates affiliate links for multiple URLs in a single API call.

**Parameters:**
- `target_urls` (list[str]): List of target URLs to generate affiliate links for

**Returns:**
- `dict[str, str | None]`: Dictionary mapping each target URL to its affiliate link

**Features:**
- Batch processing for efficiency
- Cache-first approach
- Automatic URL prefixing for AliExpress share format
- Comprehensive error handling

**Example:**
```python
urls = [
    "https://www.aliexpress.com/item/123.html",
    "https://www.aliexpress.com/item/456.html"
]
affiliate_links = await generate_affiliate_links_batch(urls)
for original_url, affiliate_link in affiliate_links.items():
    print(f"Original: {original_url}")
    print(f"Affiliate: {affiliate_link}")
```

### Telegram Bot Handlers

#### `async start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None`

Handles the `/start` command and sends a welcome message to users.

**Parameters:**
- `update` (Update): Telegram update object
- `context` (ContextTypes.DEFAULT_TYPE): Telegram context object

**Example Response:**
```
👋 Welcome to the AliExpress Discount Bot! 🛍️

🔍 How to use this bot:
1️⃣ Copy a product link from AliExpress 📋
2️⃣ Send the link to this bot 📤
3️⃣ The bot will automatically generate affiliate links for you ✨
4️⃣ Use the links to share and earn 💰

🔗 Supported link types:
• Regular AliExpress product links 🌐
• Shortened AliExpress links 🔄

🚀 Send any AliExpress product link now to try the bot! 🎁
```

#### `async process_product_telegram(product_id: str, base_url: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None`

Processes a product ID, fetches details, generates affiliate links, and sends a formatted response.

**Parameters:**
- `product_id` (str): The AliExpress product ID
- `base_url` (str): The base product URL
- `update` (Update): Telegram update object
- `context` (ContextTypes.DEFAULT_TYPE): Telegram context object

**Features:**
- API-first approach with scraping fallback
- Multiple offer types (coin, super, limited, bigsave)
- Rich HTML formatting
- Image inclusion when available
- Comprehensive error handling

**Response Format:**
```
[Product Title]

Sale Price: $29.99 USD

Offers:
💰 Coin Offers: [Click Here]
⚡ Super Deals: [Click Here]
⏰ Limited Time: [Click Here]
💸 Big Save: [Click Here]
```

#### `async handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None`

Main message handler that processes incoming messages and extracts AliExpress URLs.

**Parameters:**
- `update` (Update): Telegram update object
- `context` (ContextTypes.DEFAULT_TYPE): Telegram context object

**Features:**
- Automatic URL detection and extraction
- Short link resolution
- Multiple URL processing in a single message
- User feedback during processing
- Error handling and user notifications

### Utility Functions

#### `async periodic_cache_cleanup(context: ContextTypes.DEFAULT_TYPE) -> None`

Periodic job that cleans expired items from all caches.

**Parameters:**
- `context` (ContextTypes.DEFAULT_TYPE): Telegram context object

**Schedule:** Runs every 6 hours

**Features:**
- Cleans product cache, link cache, and resolved URL cache
- Logs cleanup statistics
- Automatic scheduling via Telegram job queue

---

## AliExpress Utilities (`aliexpress_utils.py`)

This module provides utility functions for scraping AliExpress product information when the API is unavailable.

### Functions

#### `get_aliexpress_product_info(product_url: str) -> tuple[str | None, str | None]`

Extracts product name and image URL from an AliExpress product page using web scraping.

**Parameters:**
- `product_url` (str): The AliExpress product page URL

**Returns:**
- `tuple[str | None, str | None]`: A tuple containing (product_name, image_url)

**Features:**
- Multiple fallback strategies for product name extraction
- Image URL extraction with fallbacks
- Automatic cleanup of product names (removes AliExpress suffixes)
- Comprehensive error handling
- Custom headers and cookies for better success rate

**Extraction Strategies (in order of preference):**
1. Specific H1 tag with CSS selector
2. OpenGraph title meta tag
3. Keywords meta tag (first keyword)
4. H1 tag with `data-pl="product-title"` attribute
5. H1 tag with product title classes
6. Generic H1 tag (fallback)

**Example:**
```python
product_name, image_url = get_aliexpress_product_info("https://www.aliexpress.com/item/123456789.html")
if product_name:
    print(f"Product: {product_name}")
if image_url:
    print(f"Image: {image_url}")
```

#### `get_product_details_by_id(product_id: str | int) -> tuple[str | None, str | None]`

Constructs a URL from a product ID and fetches product details using web scraping.

**Parameters:**
- `product_id` (str | int): The AliExpress product ID

**Returns:**
- `tuple[str | None, str | None]`: A tuple containing (product_name, image_url)

**URL Format:** `https://vi.aliexpress.com/item/{product_id}.html`

**Example:**
```python
product_name, image_url = get_product_details_by_id("1234567890")
if product_name:
    print(f"Product: {product_name}")
```

**Error Handling:**
- Network timeouts (15 seconds)
- HTTP errors (non-200 status codes)
- Parsing errors (malformed HTML)
- Returns `(None, None)` on any error

---

## IOP SDK Module (`iop/`)

The IOP (International Open Platform) SDK module provides the interface for communicating with AliExpress APIs.

### Classes

#### `IopRequest`

Represents an API request to the AliExpress platform.

**Constructor:**
```python
IopRequest(api_name: str, http_method: str = 'POST')
```

**Parameters:**
- `api_name` (str): The API method name (e.g., 'aliexpress.affiliate.productdetail.get')
- `http_method` (str): HTTP method to use (default: 'POST')

**Methods:**

##### `add_api_param(key: str, value: str) -> None`
Adds an API parameter to the request.

**Parameters:**
- `key` (str): Parameter name
- `value` (str): Parameter value

**Example:**
```python
request = IopRequest('aliexpress.affiliate.productdetail.get')
request.add_api_param('product_ids', '1234567890')
request.add_api_param('fields', 'product_title,target_sale_price')
```

##### `add_file_param(key: str, value: Any) -> None`
Adds a file parameter to the request (for file uploads).

**Parameters:**
- `key` (str): Parameter name
- `value` (Any): File object or file data

##### `set_simplify() -> None`
Enables simplified response format.

**Example:**
```python
request.set_simplify()  # Response will be in simplified format
```

##### `set_format(value: str) -> None`
Sets the response format.

**Parameters:**
- `value` (str): Format type (e.g., 'json', 'xml')

**Example:**
```python
request.set_format('json')  # Default format
```

#### `IopResponse`

Represents an API response from the AliExpress platform.

**Attributes:**
- `type` (str | None): Response type
- `code` (str | None): Response code
- `message` (str | None): Response message
- `request_id` (str | None): Unique request identifier
- `body` (dict | None): Response body data

**Methods:**

##### `__str__() -> str`
Returns a string representation of the response.

**Example:**
```python
response = client.execute(request)
print(response)  # Output: type=SUCCESS code=0 message=success requestId=abc123
```

#### `IopClient`

Main client for executing API requests to AliExpress.

**Constructor:**
```python
IopClient(server_url: str, app_key: str, app_secret: str, timeout: int = 30)
```

**Parameters:**
- `server_url` (str): API server URL (e.g., 'https://api-sg.aliexpress.com/sync')
- `app_key` (str): Application key from AliExpress
- `app_secret` (str): Application secret from AliExpress
- `timeout` (int): Request timeout in seconds (default: 30)

**Class Attributes:**
- `log_level` (str): Logging level ('DEBUG', 'INFO', 'ERROR')

**Methods:**

##### `execute(request: IopRequest, access_token: str = None) -> IopResponse`
Executes an API request and returns the response.

**Parameters:**
- `request` (IopRequest): The request object to execute
- `access_token` (str, optional): Access token for authenticated requests

**Returns:**
- `IopResponse`: The API response object

**Features:**
- Automatic request signing using HMAC-SHA256
- Comprehensive logging
- Error handling and reporting
- Support for both GET and POST requests
- File upload support

**Example:**
```python
# Initialize client
client = IopClient(
    'https://api-sg.aliexpress.com/sync',
    'your_app_key',
    'your_app_secret'
)

# Create request
request = IopRequest('aliexpress.affiliate.productdetail.get')
request.add_api_param('product_ids', '1234567890')
request.add_api_param('fields', 'product_title,target_sale_price')
request.add_api_param('target_currency', 'USD')

# Execute request
response = client.execute(request)

# Process response
if response.code == '0':
    print("Success:", response.body)
else:
    print("Error:", response.message)
```

### Utility Functions

#### `sign(secret: str, api: str, parameters: dict) -> str`

Generates HMAC-SHA256 signature for API authentication.

**Parameters:**
- `secret` (str): Application secret
- `api` (str): API method name
- `parameters` (dict): Request parameters

**Returns:**
- `str`: Uppercase hexadecimal signature

**Example:**
```python
signature = sign('your_secret', 'aliexpress.affiliate.productdetail.get', {'param1': 'value1'})
```

#### `logApiError(appkey: str, sdkVersion: str, requestUrl: str, code: str, message: str) -> None`

Logs API errors with system information.

**Parameters:**
- `appkey` (str): Application key
- `sdkVersion` (str): SDK version
- `requestUrl` (str): Request URL
- `code` (str): Error code
- `message` (str): Error message

---

## Keep Alive Module (`keep_alive.py`)

This module provides a simple Flask web server for keeping the application alive on hosting platforms.

### Flask Application

#### Routes

##### `GET /`
Returns a simple response to indicate the service is running.

**Response:** `"?"`

**Example:**
```bash
curl http://localhost:8080/
# Response: ?
```

### Functions

#### `run() -> None`
Starts the Flask web server.

**Configuration:**
- Host: `0.0.0.0` (accepts connections from any IP)
- Port: `8080`

#### `keep_alive() -> None`
Starts the Flask server in a separate thread.

**Features:**
- Non-blocking execution (runs in background thread)
- Automatic startup when module is imported

#### `self_ping() -> None`
Continuously pings the application to keep it alive on hosting platforms.

**Configuration:**
- Target URL: `https://aliexpress-telegram-bot-2t8i.onrender.com`
- Ping interval: 3 minutes (180 seconds)
- Runs indefinitely in a loop

**Features:**
- Error handling for failed ping attempts
- Logging of ping status
- Automatic restart on exceptions

**Example Usage:**
```python
from keep_alive import keep_alive

# Start the keep-alive server
keep_alive()

# Your main application code here
```

---

## Configuration

### Environment Variables

The application requires the following environment variables:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from BotFather | Yes | - |
| `ALIEXPRESS_APP_KEY` | AliExpress API application key | Yes | - |
| `ALIEXPRESS_APP_SECRET` | AliExpress API application secret | Yes | - |
| `ALIEXPRESS_TRACKING_ID` | AliExpress affiliate tracking ID | No | "default" |
| `TARGET_CURRENCY` | Target currency for prices | No | "USD" |
| `TARGET_LANGUAGE` | Target language for content | No | "en" |
| `QUERY_COUNTRY` | Target country for queries | No | "US" |

### Cache Configuration

```python
CACHE_EXPIRY_DAYS = 1  # Cache expiry in days
CACHE_EXPIRY_SECONDS = CACHE_EXPIRY_DAYS * 24 * 60 * 60  # 86400 seconds
```

### Offer Types

The bot supports four types of offers with specific URL parameters:

```python
OFFER_PARAMS = {
    "coin": {
        "name": "💰 Coin Offers",
        "params": {"af": "1", "cv": "47843", "dp": "v5_47843", "utm_source": "admitad", "utm_medium": "cpa", "utm_campaign": "47843"}
    },
    "super": {
        "name": "⚡ Super Deals", 
        "params": {"af": "1", "cv": "47843", "dp": "v5_47843", "utm_source": "admitad", "utm_medium": "cpa", "utm_campaign": "47843", "super": "1"}
    },
    "limited": {
        "name": "⏰ Limited Time",
        "params": {"af": "1", "cv": "47843", "dp": "v5_47843", "utm_source": "admitad", "utm_medium": "cpa", "utm_campaign": "47843", "limited": "1"}
    },
    "bigsave": {
        "name": "💸 Big Save",
        "params": {"af": "1", "cv": "47843", "dp": "v5_47843", "utm_source": "admitad", "utm_medium": "cpa", "utm_campaign": "47843", "bigsave": "1"}
    }
}
```