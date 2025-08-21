import json
import os
from typing import List

FILE_PATH = os.getenv("SUBSCRIBERS_FILE", "subscribers.json")


def _ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)


def list_subscribers() -> List[int]:
    if not os.path.exists(FILE_PATH):
        return []
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return [int(x) for x in data]
    except Exception:
        pass
    return []


def add_subscriber(chat_id: int) -> bool:
    subs = set(list_subscribers())
    if chat_id in subs:
        return False
    subs.add(int(chat_id))
    _ensure_parent_dir(FILE_PATH)
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted(list(subs)), f)
    return True


def remove_subscriber(chat_id: int) -> bool:
    subs = set(list_subscribers())
    if chat_id not in subs:
        return False
    subs.remove(int(chat_id))
    _ensure_parent_dir(FILE_PATH)
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted(list(subs)), f)
    return True