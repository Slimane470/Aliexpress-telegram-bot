from dataclasses import dataclass
from typing import Iterable, List, Sequence


@dataclass
class Deal:
    title: str
    url: str
    price: float
    category: str


def fetch_top_deals(limit: int = 10) -> List[Deal]:
    demo: List[Deal] = [
        Deal(title="Wireless Earbuds ANC", url="https://aliexpress.com/item/123", price=19.99, category="electronics"),
        Deal(title="Robot Vacuum Cleaner", url="https://aliexpress.com/item/234", price=129.0, category="home"),
        Deal(title="USB-C Fast Charger 45W", url="https://aliexpress.com/item/345", price=9.5, category="electronics"),
        Deal(title="Sport Smartwatch", url="https://aliexpress.com/item/456", price=24.99, category="wearables"),
        Deal(title="4K HDMI Cable", url="https://aliexpress.com/item/567", price=3.49, category="accessories"),
        Deal(title="Portable Blender", url="https://aliexpress.com/item/678", price=15.0, category="kitchen"),
        Deal(title="LED Strip Lights", url="https://aliexpress.com/item/789", price=7.99, category="home"),
    ]
    return demo[:limit]


def filter_deals(
    deals: Sequence[Deal],
    categories: Iterable[str],
    min_price: float,
    limit: int = 5,
) -> List[Deal]:
    normalized_cats = {c.strip().lower() for c in categories if c.strip()}
    filtered: List[Deal] = []
    for d in deals:
        if d.price < float(min_price):
            continue
        if normalized_cats and d.category.lower() not in normalized_cats:
            continue
        filtered.append(d)
    filtered.sort(key=lambda d: d.price)
    return filtered[:limit]