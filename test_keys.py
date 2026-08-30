import asyncio
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from bot.services.llm_router import llm_router
from bot.services.memory import memory

async def run_diagnostics():
    print("\n" + "=" * 60)
    print("🔍 ПЕРЕВІРКА API КЛЮЧІВ ТА ПРОВАЙДЕРІВ ДЛЯ БОТА «ЩУРМАН»")
    print("=" * 60)

    await memory.init_db()

    results = await llm_router.check_all_keys()
    all_ok = False
    for name, info in results.items():
        print(f"\n[{name.upper()}] - {info['display_name']}")
        print(f"Статус: {info['status']}")
        if info['ok']:
            all_ok = True

    print("\n" + "=" * 60)
    if all_ok:
        print("✅ Щонайменше один провайдер працює коректно! Бот зможе відповідати.")
    else:
        print("⚠️ УВАГА: Жоден провайдер не зміг дати успішну відповідь. Перевірте ключі в .env файлі.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    asyncio.run(run_diagnostics())
