import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from bot.config import settings
from bot.services.memory import memory
from bot.services.llm_router import llm_router

logger = logging.getLogger(__name__)
router = Router()

def is_admin(user_id: int) -> bool:
    return user_id in settings.admin_id_list

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    if not is_admin(message.from_user.id):
        return

    stats = await memory.get_stats()
    text = (
        f"📊 **Статистика бота «Щурман»**\n\n"
        f"💬 **Всього повідомлень:** `{stats['total_messages']}`\n"
        f"👥 **Активних чатів:** `{stats['total_chats']}`\n\n"
        f"🤖 **Використання AI-провайдерів:**\n"
    )

    if not stats["provider_stats"]:
        text += "_Поки що немає даних викликів._\n"
    else:
        for p in stats["provider_stats"]:
            text += (
                f"• **{p['provider'].upper()}**:\n"
                f"  - Всього викликів: `{p['total']}`\n"
                f"  - Успішних: `{p['success']}` ({p['success_rate']})\n"
                f"  - Помилок/лімітів: `{p['failed']}`\n"
            )

    await message.answer(text, parse_mode="Markdown")

@router.message(Command("check_keys"))
async def cmd_check_keys(message: Message):
    if not is_admin(message.from_user.id):
        return

    status_msg = await message.answer("🔍 Перевіряю працездатність усіх підключених API ключів... Зачекайте.")
    try:
        results = await llm_router.check_all_keys()
        text = "🔑 **Результати діагностики API Ключів:**\n\n"
        for name, info in results.items():
            text += f"• **{info['display_name']}**:\n  {info['status']}\n\n"

        await status_msg.edit_text(text, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error checking keys: {e}")
        await status_msg.edit_text(f"❌ Помилка під час діагностики: `{e}`", parse_mode="Markdown")
