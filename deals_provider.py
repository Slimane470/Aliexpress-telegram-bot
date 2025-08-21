from dataclasses import dataclass
from typing import List


@dataclass
class Deal:
    title: str
    url: str
    price: float
    category: str


def fetch_top_deals(limit: int = 10) -> List[Deal]:
    demo: List[Deal] = [
        Deal(title="🔥 Wireless Earbuds ANC", url="https://s.click.aliexpress.com/e/_oF7fTq1", price=19.99, category="electronics"),
        Deal(title="🤖 Robot Vacuum Cleaner", url="https://s.click.aliexpress.com/e/_oE9rQxJ", price=129.0, category="home"),
        Deal(title="⚡ USB-C Fast Charger 45W", url="https://s.click.aliexpress.com/e/_oD2VQ7b", price=9.5, category="electronics"),
        Deal(title="⌚ Sport Smartwatch", url="https://s.click.aliexpress.com/e/_oE1cH8n", price=24.99, category="wearables"),
        Deal(title="📺 4K HDMI Cable", url="https://s.click.aliexpress.com/e/_omzJvQv", price=3.49, category="accessories"),
        Deal(title="🥤 Portable Blender", url="https://s.click.aliexpress.com/e/_oCz8k7L", price=15.0, category="kitchen"),
        Deal(title="✨ LED Strip Lights", url="https://s.click.aliexpress.com/e/_oB7gS9Z", price=7.99, category="home"),
        Deal(title="🎮 Game Controller", url="https://s.click.aliexpress.com/e/_oE4N2Q3", price=17.49, category="electronics"),
    ]
    return demo[:limit]