from __future__ import annotations

import os
import ujson as json
from typing import Optional, Sequence, List
from . import DealsProvider, Deal


class SampleDealsProvider(DealsProvider):
    def __init__(self, json_path: str) -> None:
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Sample deals JSON not found: {json_path}")
        self.json_path = json_path

    def fetch_deals(
        self, category: Optional[str] = None, max_price: Optional[float] = None, limit: int = 10
    ) -> Sequence[Deal]:
        with open(self.json_path, "r", encoding="utf-8") as f:
            raw: List[dict] = json.load(f)

        deals: List[Deal] = []
        for item in raw:
            try:
                deal = Deal(
                    id=str(item.get("id")),
                    title=str(item.get("title")),
                    price=float(item.get("price")),
                    currency=str(item.get("currency", "USD")),
                    url=str(item.get("url")),
                    image_url=item.get("image_url"),
                    category=item.get("category"),
                    discount_text=item.get("discount_text"),
                )
            except Exception:
                continue

            if category and deal.category and deal.category.lower() != category.lower():
                continue
            if max_price is not None and deal.price > max_price:
                continue
            deals.append(deal)

        deals.sort(key=lambda d: d.price)
        return deals[:limit]