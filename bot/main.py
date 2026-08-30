import asyncio
import logging
import sys
import os
from pathlib import Path

# Додаємо корінь проєкту до sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.config import settings
from bot.services.memory import memory
from bot.handlers import main_router

# Налаштування логування
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - [%(levelname)s] - %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("mops_bot")

async def set_bot_commands(bot: Bot):
    """Встановлення меню команд у Telegram клієнті."""
    commands = [
        BotCommand(command="start", description="🚀 Запустити бота та інтро"),
        BotCommand(command="los", description="💥 Зарядити лося Мопсу за донат"),
        BotCommand(command="lyash", description="👋 Прописати сочного ляща"),
        BotCommand(command="chifir", description="☕ Заварити ядрьоний чифір"),
        BotCommand(command="donat", description="💸 Донат на м'ясо і папіроси"),
        BotCommand(command="role", description="🎭 Обрати масть/роль"),
        BotCommand(command="model", description="⚙️ Налаштувати AI модель"),
        BotCommand(command="reset", description="🧹 Очистити пам'ять бесіди"),
        BotCommand(command="help", description="📖 Довідка та команди"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())

async def main():
    logger.info("=" * 50)
    logger.info("Запуск Telegram-бота «Мопс дядя Пёс (Гав, Гав!)»...")
    logger.info("=" * 50)

    # 1. Ініціалізація бази даних SQLite
    await memory.init_db()

    # 2. Створення бота та диспетчера
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=None)
    )
    dp = Dispatcher()
    dp.include_router(main_router)

    # 3. Реєстрація команд в меню
    try:
        await set_bot_commands(bot)
        logger.info("Меню команд бота успішно зареєстровано в Telegram.")
    except Exception as e:
        logger.warning(f"Не вдалося встановити команди меню: {e}")

    # 4. Отримання інфо про бота
    try:
        bot_info = await bot.get_me()
        logger.info(f"Бот успішно підключився: @{bot_info.username} (ID: {bot_info.id})")
        logger.info("Мопс дядя Пёс готовий до роботи 24/7!")
    except Exception as e:
        logger.error(f"Помилка авторизації токена бота в Telegram: {e}")
        return

    # 5. Запуск Long Polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot,
            allowed_updates=["message", "channel_post", "callback_query", "chat_member", "my_chat_member"]
        )
    finally:
        logger.info("Зупинка бота Мопс дядя Пёс...")
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот зупинений користувачем.")
