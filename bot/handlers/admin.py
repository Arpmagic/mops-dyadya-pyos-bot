import logging
import aiogram
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

@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message, bot: aiogram.Bot):
    if not is_admin(message.from_user.id):
        return

    text_to_send = message.text.replace("/broadcast", "").strip()
    if not text_to_send and not message.photo and not message.video:
        await message.answer("⚠️ Введіть текст, фото або відео для розсилки.\nПриклад: `/broadcast Усім привіт!`")
        return

    chats = await memory.get_all_chats()
    if not chats:
        await message.answer("База чатів порожня.")
        return

    await message.answer(f"🚀 Починаю розсилку для {len(chats)} чатів...")
    
    success, failed = 0, 0
    for chat_id in chats:
        try:
            if message.photo:
                await bot.send_photo(chat_id, message.photo[-1].file_id, caption=message.caption)
            elif message.video:
                await bot.send_video(chat_id, message.video.file_id, caption=message.caption)
            else:
                await bot.send_message(chat_id, text_to_send)
            success += 1
        except Exception:
            failed += 1

    await message.answer(f"✅ **Розсилка завершена!**\nУспішно: `{success}`\nПомилок: `{failed}`", parse_mode="Markdown")
