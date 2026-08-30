import logging
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, Update
from cachetools import TTLCache

logger = logging.getLogger(__name__)

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 3.0):
        # Кеш на 1000 юзерів, час життя запису = rate_limit секунд
        self.cache = TTLCache(maxsize=1000, ttl=rate_limit)

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        user_id = event.from_user.id if event.from_user else None
        if user_id:
            if user_id in self.cache:
                # Юзер спамить, відхиляємо запит
                logger.warning(f"Throttling triggered for user {user_id}")
                try:
                    await event.reply("🚫 В чергу, падлюки, я один! Почекай пару секунд.")
                except Exception:
                    pass
                return
            
            # Додаємо юзера в кеш
            self.cache[user_id] = True

        return await handler(event, data)
