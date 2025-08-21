from typing import Optional, Sequence
from ..config import get_settings
from .providers import Deal, DealsProvider
from .providers.sample import SampleDealsProvider


def create_provider() -> DealsProvider:
    settings = get_settings()
    provider_name = settings.provider.lower()
    if provider_name == "sample":
        return SampleDealsProvider(settings.sample_deals_json)
    raise ValueError(f"Unsupported provider: {settings.provider}")


def fetch_deals(category: Optional[str], max_price: Optional[float], limit: int = 10) -> Sequence[Deal]:
    provider = create_provider()
    return provider.fetch_deals(category=category, max_price=max_price, limit=limit)