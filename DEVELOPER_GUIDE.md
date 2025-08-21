# AliExpress Telegram Bot - Developer Guide

## Quick Reference

### Project Structure

```
├── app.py                 # Main application with bot logic
├── aliexpress_utils.py    # Web scraping utilities
├── keep_alive.py          # Flask server for hosting platforms
├── iop/                   # AliExpress API SDK
│   ├── __init__.py
│   └── base.py           # Core SDK classes
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── .env                  # Environment variables (create this)
└── README.md             # Project documentation
```

### Core Components

| Component | Purpose | Key Functions |
|-----------|---------|---------------|
| `CacheWithExpiry` | Async caching with TTL | `get()`, `set()`, `clear_expired()` |
| `IopClient` | AliExpress API client | `execute()` |
| `IopRequest` | API request builder | `add_api_param()` |
| Bot handlers | Telegram integration | `start()`, `handle_message()` |

### Quick Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
export TELEGRAM_BOT_TOKEN="your_token"
export ALIEXPRESS_APP_KEY="your_key"
export ALIEXPRESS_APP_SECRET="your_secret"

# 3. Run the bot
python app.py
```

## Key APIs

### Product Processing Flow

```python
# 1. Extract product ID from URL
product_id = extract_product_id(url)

# 2. Fetch product details (API + scraping fallback)
details = await fetch_product_details_v2(product_id)

# 3. Generate affiliate links for different offers
target_urls = [build_url_with_offer_params(base_url, params) for params in offers]
affiliate_links = await generate_affiliate_links_batch(target_urls)

# 4. Send formatted response to user
await send_product_response(update, details, affiliate_links)
```

### Essential Functions

```python
# URL Processing
product_id = extract_product_id(url)                    # Extract ID from URL
urls = extract_potential_aliexpress_urls(text)          # Find URLs in text
final_url = await resolve_short_link(short_url, session) # Resolve shortened URLs

# Product Data
details = await fetch_product_details_v2(product_id)    # Get product info (API)
name, image = get_product_details_by_id(product_id)     # Get product info (scraping)

# Affiliate Links
links = await generate_affiliate_links_batch(urls)      # Generate affiliate links

# Caching
value = await cache.get(key)                            # Get from cache
await cache.set(key, value)                             # Store in cache
```

## Configuration

### Environment Variables

```bash
# Required
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ALIEXPRESS_APP_KEY=12345
ALIEXPRESS_APP_SECRET=abcdef123456

# Optional
ALIEXPRESS_TRACKING_ID=default
TARGET_CURRENCY=USD
TARGET_LANGUAGE=en
QUERY_COUNTRY=US
```

### Offer Configuration

```python
OFFER_PARAMS = {
    "coin": {"name": "💰 Coin Offers", "params": {...}},
    "super": {"name": "⚡ Super Deals", "params": {...}},
    "limited": {"name": "⏰ Limited Time", "params": {...}},
    "bigsave": {"name": "💸 Big Save", "params": {...}}
}
```

## Common Patterns

### Async Error Handling

```python
try:
    result = await api_call()
    if result:
        return process_result(result)
    else:
        logger.warning("API returned no data")
        return fallback_method()
except Exception as e:
    logger.error(f"API error: {e}")
    return None
```

### Cache Pattern

```python
async def get_with_cache(key, fetch_func):
    # Check cache first
    cached = await cache.get(key)
    if cached:
        return cached
    
    # Fetch and cache
    data = await fetch_func()
    if data:
        await cache.set(key, data)
    return data
```

### Batch Processing

```python
async def process_batch(items):
    tasks = [process_single_item(item) for item in items]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle results and exceptions
    successful = [r for r in results if not isinstance(r, Exception)]
    failed = [r for r in results if isinstance(r, Exception)]
    
    return successful, failed
```

## Testing

### Unit Tests

```python
import pytest
import asyncio
from app import extract_product_id, CacheWithExpiry

def test_extract_product_id():
    url = "https://www.aliexpress.com/item/1234567890.html"
    assert extract_product_id(url) == "1234567890"

@pytest.mark.asyncio
async def test_cache():
    cache = CacheWithExpiry(60)  # 1 minute expiry
    await cache.set("test", "value")
    assert await cache.get("test") == "value"
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_product_processing():
    product_id = "1234567890"
    details = await fetch_product_details_v2(product_id)
    assert details is not None
    assert "title" in details
    assert "price" in details
```

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "app.py"]
```

### Environment Setup

```bash
# Development
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Production
gunicorn --bind 0.0.0.0:8080 app:app  # If using Flask mode
# or
python app.py  # Direct execution
```

## Monitoring

### Logging

```python
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Usage
logger.info(f"Processing product {product_id}")
logger.warning(f"API fallback for product {product_id}")
logger.error(f"Failed to process product {product_id}: {error}")
```

### Metrics

```python
# Track important metrics
cache_hits = 0
cache_misses = 0
api_calls = 0
api_failures = 0
processed_products = 0

# Log metrics periodically
logger.info(f"Cache hit rate: {cache_hits/(cache_hits+cache_misses)*100:.1f}%")
logger.info(f"API success rate: {(api_calls-api_failures)/api_calls*100:.1f}%")
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Bot not responding | Invalid token | Check `TELEGRAM_BOT_TOKEN` |
| API errors | Invalid credentials | Verify `ALIEXPRESS_APP_KEY/SECRET` |
| No product details | Product not found | Check product ID extraction |
| Memory issues | Cache growth | Enable periodic cleanup |
| Slow responses | No caching | Verify cache configuration |

### Debug Commands

```python
# Enable debug logging
logging.getLogger().setLevel(logging.DEBUG)

# Test individual components
product_id = extract_product_id(url)
print(f"Extracted ID: {product_id}")

details = await fetch_product_details_v2(product_id)
print(f"Product details: {details}")

# Check cache status
print(f"Cache size: {len(cache.cache)}")
```

## Performance Tips

1. **Use batch operations** for multiple products
2. **Enable caching** with appropriate TTL
3. **Handle errors gracefully** with fallbacks
4. **Monitor API rate limits** 
5. **Use connection pooling** for HTTP requests
6. **Clean up resources** regularly

## Security Notes

- Never log sensitive credentials
- Validate all user inputs
- Use environment variables for secrets
- Implement rate limiting for user requests
- Sanitize URLs before processing

## Extension Points

### Adding New Offer Types

```python
OFFER_PARAMS["new_offer"] = {
    "name": "🎯 New Offer",
    "params": {"custom_param": "value"}
}
OFFER_ORDER.append("new_offer")
```

### Custom Product Processors

```python
async def custom_product_processor(product_id):
    # Custom logic here
    return custom_details

# Register processor
product_processors = {
    "custom": custom_product_processor
}
```

### Additional Bot Commands

```python
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Custom response")

# Register command
application.add_handler(CommandHandler("custom", custom_command))
```

This developer guide provides quick access to essential information for developing and maintaining the AliExpress Telegram Bot.