from dataclasses import dataclass
from typing import Optional, Sequence


@dataclass
class Deal:
    id: str
    title: str
    price: float
    currency: str
    url: str
    image_url: Optional[str] = None
    category: Optional[str] = None
    discount_text: Optional[str] = None


class DealsProvider:
    def fetch_deals(
        self, category: Optional[str] = None, max_price: Optional[float] = None, limit: int = 10
    ) -> Sequence[Deal]:
        raise NotImplementedError