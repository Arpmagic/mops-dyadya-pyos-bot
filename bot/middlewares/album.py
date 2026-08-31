import asyncio
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, Update

class AlbumMiddleware(BaseMiddleware):
    def __init__(self, latency: float = 0.5):
        self.latency = latency
        self.album_data = {}

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        if not getattr(event, 'media_group_id', None):
            return await handler(event, data)

        try:
            self.album_data[event.media_group_id].append(event)
            return  # Drop subsequent messages
        except KeyError:
            self.album_data[event.media_group_id] = [event]
            await asyncio.sleep(self.latency)
            
            data['album'] = self.album_data[event.media_group_id]
            result = await handler(event, data)
            if event.media_group_id in self.album_data:
                del self.album_data[event.media_group_id]
            return result
