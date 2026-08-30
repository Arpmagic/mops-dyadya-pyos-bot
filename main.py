"""
Головна точка входу для запуску Telegram-бота «Мопс дядя Пёс».
"""
import asyncio
from bot.main import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
