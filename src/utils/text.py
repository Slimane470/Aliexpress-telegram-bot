from typing import Iterable
from ..deals.providers import Deal


def escape_md(text: str) -> str:
    specials = "_[]()~`>#+-=|{}.!"
    escaped = ""
    for ch in text:
        if ch in specials:
            escaped += "\\" + ch
        else:
            escaped += ch
    return escaped


def format_deal_md(deal: Deal) -> str:
    title = escape_md(deal.title)
    price = f"{deal.price:.2f} {deal.currency}"
    parts = [
        f"• *{title}*",
        f"  Price: `{price}`",
    ]
    if deal.discount_text:
        parts.append(f"  Discount: {escape_md(deal.discount_text)}")
    parts.append(f"  Link: {escape_md(deal.url)}")
    return "\n".join(parts)


def format_deals_md(deals: Iterable[Deal]) -> str:
    lines = []
    for deal in deals:
        lines.append(format_deal_md(deal))
        lines.append("")
    return "\n".join(lines).strip()