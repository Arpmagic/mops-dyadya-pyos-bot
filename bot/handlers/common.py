import random
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, LinkPreviewOptions
from aiogram.exceptions import TelegramBadRequest
from bot.prompts.personas import PERSONAS, get_role_info
from bot.services.memory import memory
from bot.handlers.messages import handle_text_message

router = Router()

async def send_reply(message: Message, text: str, reply_markup=None):
    """Відправляє відповідь строго в тред повідомлення/коментарів з відключеним прев'ю посилань."""
    no_preview = LinkPreviewOptions(is_disabled=True)
    try:
        await message.reply(text, reply_markup=reply_markup, parse_mode="Markdown", link_preview_options=no_preview)
    except TelegramBadRequest:
        await message.reply(text, reply_markup=reply_markup, link_preview_options=no_preview)

def get_role_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for key, val in PERSONAS.items():
        buttons.append([
            InlineKeyboardButton(
                text=f"{val['emoji']} {val['name']}",
                callback_data=f"set_role:{key}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_model_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🔄 Авто-ротація (Рекомендовано)", callback_data="set_model:auto")],
        [
            InlineKeyboardButton(text="⚡ DeepSeek V3", callback_data="set_model:deepseek"),
            InlineKeyboardButton(text="🧠 OpenAI GPT-4o", callback_data="set_model:openai"),
        ],
        [
            InlineKeyboardButton(text="🎭 Claude 3.5 Haiku", callback_data="set_model:anthropic"),
            InlineKeyboardButton(text="💎 Gemini 3.5 Flash", callback_data="set_model:gemini"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.message(CommandStart())
async def cmd_start(message: Message):
    current_role = await memory.get_chat_role(message.chat.id)
    role_info = get_role_info(current_role)

    text = (
        f"🐶 **Вечер в хату, часик в радость!**\n\n"
        f"Я — **Мопс дядя Пёс (Гав, Гав!)**. Отсидел своё по лагерям, откинулся и теперь тут с вами на стриме со Щадило!\n\n"
        f"🎯 **Поточний режим:** {role_info['emoji']} *{role_info['name']}*\n"
        f"📝 _{role_info['description']}_\n\n"
        f"💡 **Команды для пацанов:**\n"
        f"• `/role` — выбрать масть/роль\n"
        f"• `/model` — настройки AI движка\n"
        f"• `/los` — зарядить лося Мопсу за донат 💥\n"
        f"• `/lyash` — прописать сочного ляща 👋\n"
        f"• `/chifir` — заварить ядрёный чифирок ☕\n"
        f"• `/donat` — сбор на мясо и сигареты 💸\n"
        f"• `/reset` — сбросить память разговора\n"
        f"• `/help` — полная справка\n\n"
        f"🦴 *В чате зови меня:* «Мопс», «Дядя Пес», «Гав-гав», тегай бота через `@` или делай Reply. **Гав, гав!**"
    )
    await send_reply(message, text)

@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        f"📖 **Справка от легендарного Мопса**\n\n"
        f"🗣️ **Как общаться:**\n"
        f"1. **В личке:** пиши что угодно — отвечу по понятиям.\n"
        f"2. **В группе / канале / коментарях:**\n"
        f"   - Упомяни *«Мопс»*, *«Дядя Пес»*, *«Гав»*, *«Щадило»*\n"
        f"   - Тегни бота через `@`\n"
        f"   - Сделай Reply (ответ) на моё сообщение.\n"
        f"   - Закажи стрим-челлендж: `Лось`, `Муха`, `Черепаха`, `Пылесос`, `Лящ`, `Шокер`, `Травмат`, `Чифир`.\n\n"
        f"🎬 **Стрим-интерактив:**\n"
        f"• `/los` — пробить лося за донат\n"
        f"• `/lyash` — прописать ляща в прямом эфире\n"
        f"• `/chifir` — подгон душевного чифира\n"
        f"• `/donat` — сбор на мясо и сигареты\n\n"
        f"🎭 **Роли (`/role`):** Мопс (Гав-Гав!), Знаток по понятиям, Прожарка, Лютый Мопс, Братва.\n\n"
        f"Фарту, масти, АУЕ! Жизнь ворам, хуй мусорам! Гав, гав!"
    )
    await send_reply(message, text)

@router.message(Command("los"))
@router.message(Command("lyash"))
@router.message(Command("chifir"))
@router.message(Command("donat"))
async def cmd_stream_events(message: Message, bot: Bot):
    """Стрім-команди динамічно обробляються через ШІ для максимальної аутентичності та контексту."""
    await handle_text_message(message, bot)

@router.message(Command("role"))
async def cmd_role(message: Message):
    current_role = await memory.get_chat_role(message.chat.id)
    role_info = get_role_info(current_role)
    text = (
        f"🎭 **Оберіть особистість для Мопса:**\n\n"
        f"Поточна роль: {role_info['emoji']} **{role_info['name']}**\n"
        f"_{role_info['description']}_"
    )
    await send_reply(message, text, reply_markup=get_role_keyboard())

@router.callback_query(F.data.startswith("set_role:"))
async def cb_set_role(callback: CallbackQuery):
    role_key = callback.data.split(":")[1]
    if role_key in PERSONAS:
        await memory.set_chat_role(callback.message.chat.id, role_key)
        role_info = PERSONAS[role_key]
        await callback.answer(f"Роль змінено на «{role_info['name']}»!")
        try:
            await callback.message.edit_text(
                f"✅ **Особистість оновлено!**\n\n"
                f"Тепер я: {role_info['emoji']} **{role_info['name']}**\n"
                f"_{role_info['description']}_\n\n"
                f"Базаримо далі по-новому. Гав-гав!",
                parse_mode="Markdown"
            )
        except TelegramBadRequest:
            pass
    else:
        await callback.answer("Невідома роль.", show_alert=True)

@router.message(Command("model"))
async def cmd_model(message: Message):
    current_mode = await memory.get_chat_model(message.chat.id)
    text = (
        f"⚙️ **Налаштування AI Моделі:**\n\n"
        f"Поточний режим: `{'Авто-ротація' if current_mode == 'auto' else current_mode}`\n\n"
        f"Ви можете вибрати автоматичне чергування (для економії лімітів і надійності) або зафіксувати улюбленого провайдера."
    )
    await send_reply(message, text, reply_markup=get_model_keyboard())

@router.callback_query(F.data.startswith("set_model:"))
async def cb_set_model(callback: CallbackQuery):
    mode = callback.data.split(":")[1]
    await memory.set_chat_model(callback.message.chat.id, mode)
    await callback.answer(f"Режим встановлено: {mode}")
    try:
        await callback.message.edit_text(
            f"✅ **Режим AI моделі оновлено!**\n\n"
            f"Поточний вибір: `{mode}`\n"
            f"Якщо провайдер буде тимчасово перевантажений, бот автоматично перемкнеться на резервний.",
            parse_mode="Markdown"
        )
    except TelegramBadRequest:
        pass

@router.message(Command("reset"))
async def cmd_reset(message: Message):
    deleted_count = await memory.clear_chat_context(message.chat.id)
    await send_reply(
        message,
        f"🧹 **Пам'ять розмови очищено!** (Видалено {deleted_count} повідомлень контексту).\n"
        f"Починаємо спілкування з чистого аркуша. Гав!"
    )
