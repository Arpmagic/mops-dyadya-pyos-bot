import re
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, LinkPreviewOptions
from aiogram.enums import ChatType, ChatAction
from aiogram.exceptions import TelegramBadRequest

from bot.config import settings
from bot.services.memory import memory
from bot.services.llm_router import llm_router
from bot.prompts.personas import get_role_prompt

logger = logging.getLogger(__name__)
router = Router()

NAME_TRIGGER_REGEX = re.compile(
    r'(?:^|[\s.,!?:;«»"\'\(\)\/])(мопс[а-яіїєґa-z]*|дядя\s*п[еёе]с[а-яіїєґa-z]*|п[еёе]с[а-яіїєґa-z]*|гав[\s,-]*гав|гав|мургав|щадил[а-яіїєґa-z]*|щурман[а-яіїєґa-z]*|кл[іиы]торчук[а-яіїєґa-z]*|кал[\s-]*кал[иыі]ч[а-яіїєґa-z]*|капрал[а-яіїєґa-z]*|туз[а-яіїєґa-z]*|нов[іиы]к[а-яіїєґa-z]*|могил[а-яіїєґa-z]*|лабрадор[а-яіїєґa-z]*|п[иыі]лесос[а-яіїєґa-z]*|черепах[а-яіїєґa-z]*|мух[а-яіїєґa-z]*|шокер[а-яіїєґa-z]*|травмат[а-яіїєґa-z]*|чиф[іиы]р[а-яіїєґa-z]*|лось|лося|лосем|лосі|л[яеє]щ[а-яіїєґa-z]*|баб[а-яіїєґa-z]*\s*вас[я-яіїєґa-z]*|donat|los|lyash|chifir|mops[a-z]*)(?:$|[\s.,!?:;«»"\'\(\)\/])',
    re.IGNORECASE
)

LEADING_CALL_REGEX = re.compile(
    r'^(?:@\w+\s*|мопс[а-яіїєґa-z]*\s*|дядя\s*п[еёе]с[а-яіїєґa-z]*\s*|п[еёе]с[а-яіїєґa-z]*\s*|щурман[а-яіїєґa-z]*\s*)[,\s:]*',
    re.IGNORECASE
)

def should_respond(message: Message, bot_id: int, bot_username: str) -> bool:
    """Визначає, чи повинен бот відповідати на це повідомлення."""
    if message.chat.type == ChatType.PRIVATE:
        return True

    # 1. Відповідь (Reply) на повідомлення бота
    if message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.id == bot_id:
        return True

    text = message.text or message.caption or ""
    if not text:
        return False

    # 2. Згадка бота через @username
    if bot_username and f"@{bot_username.lower()}" in text.lower():
        return True

    # 3. Звернення за ім'ям або тригером
    if NAME_TRIGGER_REGEX.search(text.strip()):
        return True

    return False

def clean_user_prompt(text: str, bot_username: str) -> str:
    """Видаляє лише звернення до бота на початку запиту, зберігаючи зміст та челенджі."""
    if bot_username:
        text = re.sub(rf"^@{re.escape(bot_username)}[,\s:]*", "", text, flags=re.IGNORECASE)
    text = LEADING_CALL_REGEX.sub("", text).strip()
    return text

async def send_split_message(message: Message, text: str):
    """Відправляє довгі повідомлення частинами (ліміт Telegram 4096 символів) з відключеним прев'ю посилань."""
    MAX_LEN = 3900
    no_preview = LinkPreviewOptions(is_disabled=True)
    if len(text) <= MAX_LEN:
        try:
            await message.reply(text, parse_mode="Markdown", link_preview_options=no_preview)
        except TelegramBadRequest:
            # Якщо виникла помилка форматування Markdown, надсилаємо як звичайний текст
            await message.reply(text, link_preview_options=no_preview)
        return

    # Розбиваємо на частини
    parts = []
    while len(text) > MAX_LEN:
        split_idx = text.rfind("\n", 0, MAX_LEN)
        if split_idx == -1:
            split_idx = MAX_LEN
        parts.append(text[:split_idx].strip())
        text = text[split_idx:].strip()
    if text:
        parts.append(text)

    for p in parts:
        try:
            await message.reply(p, parse_mode="Markdown", link_preview_options=no_preview)
        except TelegramBadRequest:
            await message.reply(p, link_preview_options=no_preview)

@router.channel_post()
async def ignore_channel_wall_posts(message: Message):
    """
    Ігноруємо прямі публікації на стіні каналу, щоб не засмічувати стрічку.
    Усі відповіді бота надсилаються виключно в коментарі (тред обговорення)!
    """
    return

@router.message(F.text)
async def handle_text_message(message: Message, bot: Bot):
    bot_user = await bot.get_me()
    logger.info(f"📨 [Чат {message.chat.id} | Тред {message.message_thread_id} | Тип {message.chat.type}] Отримано: {message.text!r}")
    
    if not should_respond(message, bot_user.id, bot_user.username):
        logger.info("Повідомлення проігноровано (не відповідає тригерам або не адресоване боту).")
        return

    user_text = message.text.strip()
    cleaned_prompt = clean_user_prompt(user_text, bot_user.username)
    if not cleaned_prompt:
        cleaned_prompt = user_text

    # Індикація друкування
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    try:
        # Отримуємо налаштування ролі та моделі для поточного чату
        current_role = await memory.get_chat_role(message.chat.id)
        router_mode = await memory.get_chat_model(message.chat.id)
        system_prompt = get_role_prompt(current_role)

        # Отримуємо історію діалогу
        history = await memory.get_context(message.chat.id)
        messages_payload = history + [{"role": "user", "content": cleaned_prompt}]

        # Генерація через LLM роутер
        response_text, provider_name, model_name = await llm_router.generate_response(
            chat_id=message.chat.id,
            user_id=message.from_user.id if message.from_user else None,
            system_prompt=system_prompt,
            messages=messages_payload,
            mode=router_mode
        )

        # Зберігаємо в пам'ять
        await memory.add_message(
            chat_id=message.chat.id,
            user_id=message.from_user.id if message.from_user else None,
            role="user",
            content=cleaned_prompt
        )
        await memory.add_message(
            chat_id=message.chat.id,
            user_id=bot_user.id,
            role="assistant",
            content=response_text,
            provider_used=provider_name
        )

        # Відправка відповіді
        await send_split_message(message, response_text)

    except Exception as e:
        logger.warning(f"AI API повернув помилку: {e}. Використовуємо відповідь із бази Мопса...")
        from bot.services.vault import get_vault_response
        fallback_text = get_vault_response(cleaned_prompt)
        
        await memory.add_message(
            chat_id=message.chat.id,
            user_id=bot_user.id,
            role="assistant",
            content=fallback_text,
            provider_used="vault"
        )
        await send_split_message(message, fallback_text)
