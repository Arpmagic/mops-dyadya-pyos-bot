import time
import logging
from typing import Dict, List, Optional
from bot.config import settings

logger = logging.getLogger(__name__)

class KeyPoolManager:
    def __init__(self):
        # Структура: { "gemini": [{"key": "...", "cooldown_until": 0, "is_dead": False}], ... }
        self.pools: Dict[str, List[Dict]] = {
            "gemini": self._parse_keys(settings.GEMINI_API_KEY),
            "deepseek": self._parse_keys(settings.DEEPSEEK_API_KEY),
            "openai": self._parse_keys(settings.OPENAI_API_KEY),
            "anthropic": self._parse_keys(settings.ANTHROPIC_API_KEY),
        }
        self.indexes: Dict[str, int] = {k: 0 for k in self.pools}

    def _parse_keys(self, raw_value: Optional[str]) -> List[Dict]:
        if not raw_value:
            return []
        keys = [k.strip() for k in raw_value.split(",") if k.strip() and not k.strip().startswith("your_")]
        return [{"key": k, "cooldown_until": 0, "is_dead": False} for k in keys]

    def add_keys(self, provider: str, keys_str: str):
        new_keys = self._parse_keys(keys_str)
        existing = {item["key"] for item in self.pools.get(provider, [])}
        for item in new_keys:
            if item["key"] not in existing:
                self.pools.setdefault(provider, []).append(item)

    def get_working_key(self, provider: str) -> Optional[str]:
        """Повертає наступний робочий ключ, який не знаходиться на кулдауні (Round-Robin)."""
        pool = self.pools.get(provider, [])
        if not pool:
            return None

        now = time.time()
        active_keys = [item for item in pool if not item["is_dead"]]
        if not active_keys:
            return None

        # Шукаємо ключ, у якого минув кулдаун
        start_idx = self.indexes.get(provider, 0)
        n = len(active_keys)

        for i in range(n):
            curr = active_keys[(start_idx + i) % n]
            if curr["cooldown_until"] <= now:
                self.indexes[provider] = (start_idx + i + 1) % n
                return curr["key"]

        # Якщо всі на кулдауні, повертаємо той, у якого найменший час очікування
        best = min(active_keys, key=lambda x: x["cooldown_until"])
        return best["key"]

    def mark_rate_limited(self, provider: str, key: str, cooldown_seconds: int = 45):
        """Позначає ключ як тимчасово обмежений (429 Too Many Requests)."""
        now = time.time()
        for item in self.pools.get(provider, []):
            if item["key"] == key:
                item["cooldown_until"] = now + cooldown_seconds
                logger.warning(f"[{provider.upper()}] Ключ {key[:8]}... на кулдауні на {cooldown_seconds} сек.")
                break

    def mark_dead(self, provider: str, key: str, reason: str = ""):
        """Позначає ключ як неробочий / з вичерпаним балансом (400/402)."""
        for item in self.pools.get(provider, []):
            if item["key"] == key:
                item["is_dead"] = True
                logger.warning(f"[{provider.upper()}] Ключ {key[:8]}... вимкнено через вичерпання балансу ({reason})")
                break

    def has_available_keys(self, provider: str) -> bool:
        return any(not item["is_dead"] for item in self.pools.get(provider, []))

key_pool = KeyPoolManager()
