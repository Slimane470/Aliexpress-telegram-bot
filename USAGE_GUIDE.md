# AliExpress Telegram Bot - Usage Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Bot](#running-the-bot)
5. [Usage Examples](#usage-examples)
6. [API Usage Examples](#api-usage-examples)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

---

## Getting Started

This AliExpress Telegram Bot automatically processes AliExpress product links and generates affiliate links with various discount offers. Users can send product links to the bot and receive formatted responses with multiple offer options.

### Key Features

- ✅ **Automatic Link Processing**: Handles both regular and shortened AliExpress URLs
- ✅ **Multiple Offer Types**: Generates 4 different types of affiliate links (Coin, Super, Limited, Big Save)
- ✅ **API + Scraping Fallback**: Uses official AliExpress API with web scraping backup
- ✅ **Smart Caching**: Reduces API calls and improves response times
- ✅ **Rich Formatting**: Sends beautifully formatted messages with product images
- ✅ **Error Handling**: Graceful handling of API failures and network issues

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- AliExpress API credentials (App Key and Secret)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd aliexpress-telegram-bot
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**
```
python-telegram-bot>=20.0
aiohttp
requests
beautifulsoup4
python-dotenv
flask
```

### Step 3: Set Up Environment Variables

Create a `.env` file in the project root:

```env
# Required
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
ALIEXPRESS_APP_KEY=your_aliexpress_app_key_here
ALIEXPRESS_APP_SECRET=your_aliexpress_app_secret_here

# Optional
ALIEXPRESS_TRACKING_ID=your_tracking_id
TARGET_CURRENCY=USD
TARGET_LANGUAGE=en
QUERY_COUNTRY=US
```

---

## Configuration

### Environment Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | `1234567890:ABC...` | ✅ |
| `ALIEXPRESS_APP_KEY` | AliExpress API application key | `12345` | ✅ |
| `ALIEXPRESS_APP_SECRET` | AliExpress API application secret | `abcdef123456` | ✅ |
| `ALIEXPRESS_TRACKING_ID` | Affiliate tracking ID | `default` | ❌ |
| `TARGET_CURRENCY` | Currency for prices | `USD`, `EUR`, `GBP` | ❌ |
| `TARGET_LANGUAGE` | Language for content | `en`, `es`, `fr` | ❌ |
| `QUERY_COUNTRY` | Target country | `US`, `GB`, `DE` | ❌ |

### Getting AliExpress API Credentials

1. Visit [AliExpress Open Platform](https://open.aliexpress.com/)
2. Register for a developer account
3. Create a new application
4. Get your App Key and App Secret from the application dashboard
5. Apply for affiliate program access if needed

### Getting Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token provided

---

## Running the Bot

### Local Development

```bash
python app.py
```

### Production Deployment

The bot includes a keep-alive mechanism for cloud hosting platforms:

#### Render.com Deployment

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set environment variables in Render dashboard
4. Deploy

#### Heroku Deployment

```bash
# Install Heroku CLI
heroku create your-app-name
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set ALIEXPRESS_APP_KEY=your_key
heroku config:set ALIEXPRESS_APP_SECRET=your_secret
git push heroku main
```

#### Docker Deployment

```bash
# Build the image
docker build -t aliexpress-bot .

# Run the container
docker run -d \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e ALIEXPRESS_APP_KEY=your_key \
  -e ALIEXPRESS_APP_SECRET=your_secret \
  -p 8080:8080 \
  aliexpress-bot
```

---

## Usage Examples

### Basic Bot Usage

#### 1. Start the Bot

Send `/start` to your bot:

**User Input:**
```
/start
```

**Bot Response:**
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

#### 2. Send a Product Link

**User Input:**
```
https://www.aliexpress.com/item/1234567890.html
```

**Bot Response:**
```
[Product Image]

Wireless Bluetooth Headphones - Premium Quality Sound

Sale Price: $29.99 USD

Offers:
💰 Coin Offers: Click Here
⚡ Super Deals: Click Here
⏰ Limited Time: Click Here
💸 Big Save: Click Here
```

#### 3. Send Multiple Links

**User Input:**
```
Check out these products:
https://www.aliexpress.com/item/1111111111.html
https://s.click.aliexpress.com/e/_ABC123
```

**Bot Response:**
```
Processing 2 AliExpress links...

[First Product Response]

[Second Product Response]
```

#### 4. Send Shortened Links

**User Input:**
```
https://s.click.aliexpress.com/e/_ABC123
```

The bot will automatically resolve the shortened URL and process the product.

---

## API Usage Examples

### Using the Core Functions Programmatically

#### Example 1: Extract Product ID

```python
from app import extract_product_id

# Regular URL
url1 = "https://www.aliexpress.com/item/1234567890.html"
product_id1 = extract_product_id(url1)
print(f"Product ID: {product_id1}")  # Output: 1234567890

# URL with parameters
url2 = "https://www.aliexpress.com/item/1234567890.html?param1=value1"
product_id2 = extract_product_id(url2)
print(f"Product ID: {product_id2}")  # Output: 1234567890
```

#### Example 2: Fetch Product Details

```python
import asyncio
from app import fetch_product_details_v2

async def get_product_info():
    product_id = "1234567890"
    details = await fetch_product_details_v2(product_id)
    
    if details:
        print(f"Title: {details['title']}")
        print(f"Price: {details['price']} {details['currency']}")
        print(f"Image: {details['image_url']}")
    else:
        print("Failed to fetch product details")

# Run the async function
asyncio.run(get_product_info())
```

#### Example 3: Generate Affiliate Links

```python
import asyncio
from app import generate_affiliate_links_batch

async def create_affiliate_links():
    target_urls = [
        "https://www.aliexpress.com/item/1111111111.html",
        "https://www.aliexpress.com/item/2222222222.html",
        "https://www.aliexpress.com/item/3333333333.html"
    ]
    
    affiliate_links = await generate_affiliate_links_batch(target_urls)
    
    for original_url, affiliate_link in affiliate_links.items():
        if affiliate_link:
            print(f"Original: {original_url}")
            print(f"Affiliate: {affiliate_link}")
            print("---")
        else:
            print(f"Failed to generate affiliate link for: {original_url}")

asyncio.run(create_affiliate_links())
```

#### Example 4: Using the Cache System

```python
import asyncio
from app import CacheWithExpiry

async def cache_example():
    # Create cache with 1 hour expiry
    cache = CacheWithExpiry(3600)
    
    # Store data
    await cache.set("user_123", {"name": "John", "preferences": ["electronics"]})
    
    # Retrieve data
    user_data = await cache.get("user_123")
    if user_data:
        print(f"User: {user_data['name']}")
    
    # Clean expired items
    removed_count = await cache.clear_expired()
    print(f"Removed {removed_count} expired items")

asyncio.run(cache_example())
```

#### Example 5: Web Scraping Fallback

```python
from aliexpress_utils import get_product_details_by_id, get_aliexpress_product_info

# Method 1: By Product ID
product_name, image_url = get_product_details_by_id("1234567890")
if product_name:
    print(f"Product: {product_name}")
    print(f"Image: {image_url}")

# Method 2: By Full URL
url = "https://www.aliexpress.com/item/1234567890.html"
product_name, image_url = get_aliexpress_product_info(url)
if product_name:
    print(f"Product: {product_name}")
    print(f"Image: {image_url}")
```

#### Example 6: Using IOP SDK Directly

```python
import iop

# Initialize client
client = iop.IopClient(
    'https://api-sg.aliexpress.com/sync',
    'your_app_key',
    'your_app_secret'
)

# Get product details
request = iop.IopRequest('aliexpress.affiliate.productdetail.get')
request.add_api_param('fields', 'product_title,target_sale_price,product_main_image_url')
request.add_api_param('product_ids', '1234567890')
request.add_api_param('target_currency', 'USD')
request.add_api_param('target_language', 'en')
request.add_api_param('tracking_id', 'your_tracking_id')

response = client.execute(request)

if response.code == '0':
    print("API Success:")
    print(response.body)
else:
    print(f"API Error: {response.message}")

# Generate affiliate link
link_request = iop.IopRequest('aliexpress.affiliate.link.generate')
link_request.add_api_param('promotion_link_type', '0')
link_request.add_api_param('source_values', 'https://www.aliexpress.com/item/1234567890.html')
link_request.add_api_param('tracking_id', 'your_tracking_id')

link_response = client.execute(link_request)
if link_response.code == '0':
    print("Link Generation Success:")
    print(link_response.body)
```

---

## Troubleshooting

### Common Issues

#### 1. Bot Not Responding

**Problem:** Bot doesn't respond to messages

**Solutions:**
- Check if the bot token is correct
- Verify the bot is running (`python app.py`)
- Check logs for error messages
- Ensure webhook is not set (for polling mode)

#### 2. API Errors

**Problem:** AliExpress API returns errors

**Solutions:**
```python
# Check API credentials
print(f"App Key: {ALIEXPRESS_APP_KEY}")
print(f"App Secret: {ALIEXPRESS_APP_SECRET[:10]}...")

# Test API connection
import iop
client = iop.IopClient(ALIEXPRESS_API_URL, ALIEXPRESS_APP_KEY, ALIEXPRESS_APP_SECRET)
client.log_level = "DEBUG"  # Enable debug logging
```

#### 3. Product Details Not Found

**Problem:** Bot can't fetch product details

**Possible Causes:**
- Product ID is invalid
- Product is not available in target country
- API rate limits exceeded
- Product is not eligible for affiliate program

**Solutions:**
- Verify product ID extraction: `extract_product_id(url)`
- Check if product exists on AliExpress
- Try web scraping fallback: `get_product_details_by_id(product_id)`

#### 4. Affiliate Link Generation Fails

**Problem:** Cannot generate affiliate links

**Solutions:**
```python
# Test affiliate link generation
import asyncio
from app import generate_affiliate_links_batch

async def test_affiliate():
    urls = ["https://www.aliexpress.com/item/1234567890.html"]
    result = await generate_affiliate_links_batch(urls)
    print(result)

asyncio.run(test_affiliate())
```

#### 5. Memory Issues

**Problem:** Bot uses too much memory

**Solutions:**
- Enable cache cleanup: The bot automatically cleans cache every 6 hours
- Reduce cache expiry time in configuration
- Monitor cache sizes:

```python
print(f"Product cache size: {len(product_cache.cache)}")
print(f"Link cache size: {len(link_cache.cache)}")
print(f"URL cache size: {len(resolved_url_cache.cache)}")
```

### Debug Mode

Enable debug logging:

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

### Log Analysis

Common log patterns:

```
# Successful processing
INFO - Processing Product ID: 1234567890 for chat 123456789
INFO - Successfully fetched details via API for product ID: 1234567890
INFO - Generated 4 affiliate links for product 1234567890

# API fallback to scraping
WARNING - API failed for product ID: 1234567890. Attempting scraping fallback.
INFO - Successfully scraped details for product ID: 1234567890

# Cache operations
DEBUG - Cache hit for key: 1234567890
DEBUG - Cached value for key: 1234567890
INFO - Cached product 1234567890 until 2024-01-15 10:30:00
```

---

## Best Practices

### 1. Error Handling

Always handle potential errors when using the API:

```python
try:
    details = await fetch_product_details_v2(product_id)
    if details:
        # Process details
        pass
    else:
        # Handle no details case
        pass
except Exception as e:
    logger.error(f"Error fetching product details: {e}")
```

### 2. Rate Limiting

Respect API rate limits:

```python
# Use batch operations when possible
urls = ["url1", "url2", "url3"]
affiliate_links = await generate_affiliate_links_batch(urls)  # Better than individual calls
```

### 3. Caching Strategy

Leverage caching for better performance:

```python
# Check cache first
cached_result = await cache.get(key)
if cached_result:
    return cached_result

# Fetch and cache
result = await expensive_operation()
await cache.set(key, result)
return result
```

### 4. Resource Management

Use proper resource management:

```python
# Use async context managers
async with aiohttp.ClientSession() as session:
    result = await resolve_short_link(url, session)

# Clean up resources
await cache.clear_expired()
```

### 5. Monitoring

Monitor bot performance:

```python
# Log important metrics
logger.info(f"Processed {processed_count} products in {elapsed_time:.2f}s")
logger.info(f"Cache hit rate: {cache_hits}/{total_requests * 100:.1f}%")
logger.info(f"API success rate: {api_successes}/{api_calls * 100:.1f}%")
```

### 6. Configuration Management

Keep configuration flexible:

```python
# Use environment variables
CACHE_EXPIRY_HOURS = int(os.getenv('CACHE_EXPIRY_HOURS', '24'))
MAX_CONCURRENT_REQUESTS = int(os.getenv('MAX_CONCURRENT_REQUESTS', '10'))
ENABLE_SCRAPING_FALLBACK = os.getenv('ENABLE_SCRAPING_FALLBACK', 'true').lower() == 'true'
```

### 7. Security

Protect sensitive information:

```python
# Never log sensitive data
logger.info(f"API call successful for app_key: {app_key[:4]}***")

# Validate input
def validate_product_id(product_id):
    if not product_id or not product_id.isdigit():
        raise ValueError("Invalid product ID")
    return product_id
```

---

## Performance Optimization

### 1. Concurrent Processing

```python
import asyncio

async def process_multiple_products(product_ids):
    tasks = [fetch_product_details_v2(pid) for pid in product_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

### 2. Connection Pooling

```python
# Reuse HTTP sessions
connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
session = aiohttp.ClientSession(connector=connector)
```

### 3. Database Integration

For high-volume usage, consider adding a database:

```python
# Example with SQLite
import aiosqlite

async def cache_to_database(product_id, details):
    async with aiosqlite.connect('cache.db') as db:
        await db.execute(
            "INSERT OR REPLACE INTO products (id, details, timestamp) VALUES (?, ?, ?)",
            (product_id, json.dumps(details), time.time())
        )
        await db.commit()
```

This comprehensive usage guide provides everything needed to understand, deploy, and extend the AliExpress Telegram Bot. For additional support, refer to the API Reference documentation or check the troubleshooting section.