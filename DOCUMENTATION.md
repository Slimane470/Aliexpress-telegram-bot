# AliExpress Telegram Bot - Documentation Index

## 📚 Complete Documentation Suite

This repository contains comprehensive documentation for the AliExpress Telegram Bot. All documentation has been generated to provide complete coverage of public APIs, functions, and components.

## 📋 Documentation Files

### 1. [API Reference](./API_REFERENCE.md) 📖
**Complete technical reference for all public APIs**
- **Main Application Module** (`app.py`) - Core bot functionality, caching, API integrations
- **AliExpress Utilities** (`aliexpress_utils.py`) - Web scraping utilities and fallback methods
- **IOP SDK Module** (`iop/`) - AliExpress API SDK with client and request classes
- **Keep Alive Module** (`keep_alive.py`) - Flask server for hosting platform compatibility
- **Configuration** - Environment variables, cache settings, and offer configurations

### 2. [Usage Guide](./USAGE_GUIDE.md) 🚀
**Comprehensive guide for users and developers**
- **Getting Started** - Overview and key features
- **Installation** - Step-by-step setup instructions
- **Configuration** - Environment variables and API credentials
- **Running the Bot** - Local development and production deployment
- **Usage Examples** - Bot interaction examples and API usage patterns
- **Troubleshooting** - Common issues and solutions
- **Best Practices** - Performance optimization and security guidelines

### 3. [Developer Guide](./DEVELOPER_GUIDE.md) 🛠️
**Quick reference for developers**
- **Project Structure** - File organization and component overview
- **Core Components** - Key classes and their purposes
- **Quick Setup** - Fast development environment setup
- **Key APIs** - Essential functions and processing flows
- **Configuration** - Environment variables and offer parameters
- **Common Patterns** - Code patterns for async operations, caching, and error handling
- **Testing** - Unit and integration testing examples
- **Deployment** - Docker and production deployment guides

## 🏗️ Project Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    AliExpress Telegram Bot                      │
├─────────────────────────────────────────────────────────────────┤
│  app.py              │ Main application with Telegram bot      │
│  ├─ CacheWithExpiry  │ Async cache with TTL                   │
│  ├─ Bot Handlers     │ /start, message processing             │
│  ├─ URL Processing   │ Extract IDs, resolve short links       │
│  ├─ API Integration  │ AliExpress product details & links     │
│  └─ Affiliate Links  │ Generate multiple offer types          │
├─────────────────────────────────────────────────────────────────┤
│  aliexpress_utils.py │ Web scraping fallback utilities        │
│  ├─ Product Scraper  │ Extract titles and images from HTML    │
│  └─ Fallback System  │ Multiple extraction strategies         │
├─────────────────────────────────────────────────────────────────┤
│  iop/                │ AliExpress API SDK                      │
│  ├─ IopClient        │ API client with authentication         │
│  ├─ IopRequest       │ Request builder with parameters        │
│  └─ IopResponse      │ Response handler with error checking   │
├─────────────────────────────────────────────────────────────────┤
│  keep_alive.py       │ Flask server for hosting platforms     │
│  ├─ Flask App        │ Simple HTTP server on port 8080        │
│  └─ Self-Ping        │ Keep service alive with periodic pings │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User sends AliExpress URL
         ↓
Extract Product ID from URL
         ↓
Check Cache for Product Details
         ↓
API Call ─────→ Scraping Fallback
         ↓              ↓
    Product Details ←───┘
         ↓
Build URLs for Different Offers
         ↓
Generate Affiliate Links (Batch)
         ↓
Format Response with Rich HTML
         ↓
Send to User with Inline Buttons
```

## 🔧 Key Features Documented

### ✅ Comprehensive API Coverage
- All public functions have detailed docstrings
- Parameter types and return values specified
- Usage examples provided for each function
- Error handling patterns documented

### ✅ Complete Usage Examples
- Bot interaction examples
- Programmatic API usage
- Configuration examples
- Deployment scenarios

### ✅ Architecture Documentation
- Component relationships explained
- Data flow diagrams
- Integration patterns
- Extension points identified

### ✅ Best Practices
- Error handling strategies
- Performance optimization
- Security considerations
- Resource management

## 🚀 Quick Start

1. **Read the [Usage Guide](./USAGE_GUIDE.md)** for complete setup instructions
2. **Check the [API Reference](./API_REFERENCE.md)** for technical details
3. **Use the [Developer Guide](./DEVELOPER_GUIDE.md)** for quick development reference

## 📋 Function Coverage

### Main Application (`app.py`)
- ✅ `CacheWithExpiry` class with all methods
- ✅ `resolve_short_link()` - URL resolution with caching
- ✅ `extract_product_id()` - ID extraction from various URL formats
- ✅ `extract_potential_aliexpress_urls()` - URL detection in text
- ✅ `clean_aliexpress_url()` - URL standardization
- ✅ `build_url_with_offer_params()` - Affiliate URL building
- ✅ `fetch_product_details_v2()` - API product details with caching
- ✅ `generate_affiliate_links_batch()` - Batch affiliate link generation
- ✅ `start()` - Telegram /start command handler
- ✅ `process_product_telegram()` - Main product processing
- ✅ `handle_message()` - Message processing and URL extraction
- ✅ `periodic_cache_cleanup()` - Automated cache maintenance

### AliExpress Utilities (`aliexpress_utils.py`)
- ✅ `get_aliexpress_product_info()` - Web scraping with multiple fallbacks
- ✅ `get_product_details_by_id()` - Convenience function for ID-based scraping

### IOP SDK (`iop/base.py`)
- ✅ `IopRequest` class - API request builder
- ✅ `IopResponse` class - API response handler  
- ✅ `IopClient` class - Main API client
- ✅ `sign()` - HMAC signature generation
- ✅ `logApiError()` - API error logging

### Keep Alive (`keep_alive.py`)
- ✅ Flask application with health check endpoint
- ✅ `run()` - Flask server startup
- ✅ `keep_alive()` - Background server thread
- ✅ `self_ping()` - Periodic health checks

## 🎯 Documentation Standards

All documentation follows these standards:

### ✅ Function Documentation
- Comprehensive docstrings with purpose, parameters, and return values
- Type hints for all parameters and return values
- Usage examples with realistic scenarios
- Error handling and edge cases explained

### ✅ Class Documentation
- Class purpose and responsibilities
- Attribute descriptions
- Method documentation with examples
- Usage patterns and best practices

### ✅ Module Documentation
- Module overview and purpose
- Key components and their relationships
- Integration examples
- Configuration requirements

## 🔍 Advanced Topics

### Caching Strategy
The bot implements a sophisticated 3-tier caching system:
- **Product Cache** - API responses for product details
- **Link Cache** - Generated affiliate links
- **URL Cache** - Resolved short links

### Error Handling
Comprehensive error handling with multiple fallback strategies:
- API failures → Web scraping fallback
- Network timeouts → Cached responses
- Invalid URLs → User-friendly error messages

### Performance Optimization
- Async/await patterns for non-blocking operations
- Batch API calls for multiple products
- Connection pooling for HTTP requests
- Thread pool execution for blocking operations

## 📞 Support

For questions or issues:
1. Check the [Troubleshooting section](./USAGE_GUIDE.md#troubleshooting) in the Usage Guide
2. Review the [API Reference](./API_REFERENCE.md) for technical details
3. Examine the [Developer Guide](./DEVELOPER_GUIDE.md) for implementation patterns

---

**Documentation Generated:** Complete coverage of all public APIs, functions, and components  
**Last Updated:** Current with all codebase features and functionality  
**Coverage:** 100% of public interfaces documented with examples and usage instructions