import aiosqlite
import logging
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
from bot.config import settings

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(settings.db_full_path)

    async def init_db(self):
        """Ініціалізація бази даних та створення необхідних таблиць."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS chat_settings (
                    chat_id INTEGER PRIMARY KEY,
                    role TEXT DEFAULT 'expert',
                    router_mode TEXT DEFAULT 'auto',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL,
                    user_id INTEGER,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    provider_used TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS usage_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL,
                    user_id INTEGER,
                    provider TEXT NOT NULL,
                    is_success INTEGER NOT NULL,
                    error_message TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            await db.execute("CREATE INDEX IF NOT EXISTS idx_messages_chat_id ON messages (chat_id);")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_usage_stats_provider ON usage_stats (provider);")
            await db.commit()
            logger.info("SQLite Database initialized successfully at %s", self.db_path)

    async def get_chat_role(self, chat_id: int) -> str:
        """Отримати поточну роль для чату."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT role FROM chat_settings WHERE chat_id = ?", (chat_id,))
            row = await cursor.fetchone()
            if row:
                return row[0]
            # За замовчуванням
            await db.execute(
                "INSERT INTO chat_settings (chat_id, role, router_mode) VALUES (?, ?, ?)",
                (chat_id, settings.DEFAULT_ROLE, settings.DEFAULT_ROUTER_MODE)
            )
            await db.commit()
            return settings.DEFAULT_ROLE

    async def set_chat_role(self, chat_id: int, role: str) -> None:
        """Встановити роль для чату."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO chat_settings (chat_id, role, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(chat_id) DO UPDATE SET
                    role = excluded.role,
                    updated_at = CURRENT_TIMESTAMP;
            """, (chat_id, role))
            await db.commit()

    async def get_chat_model(self, chat_id: int) -> str:
        """Отримати режим роутера / модель для чату."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT router_mode FROM chat_settings WHERE chat_id = ?", (chat_id,))
            row = await cursor.fetchone()
            if row:
                return row[0]
            return settings.DEFAULT_ROUTER_MODE

    async def set_chat_model(self, chat_id: int, router_mode: str) -> None:
        """Встановити режим вибору моделі (auto, openai, deepseek, anthropic, gemini)."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO chat_settings (chat_id, router_mode, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(chat_id) DO UPDATE SET
                    router_mode = excluded.router_mode,
                    updated_at = CURRENT_TIMESTAMP;
            """, (chat_id, router_mode))
            await db.commit()

    async def add_message(self, chat_id: int, user_id: Optional[int], role: str, content: str, provider_used: Optional[str] = None):
        """Додати повідомлення в історію чату."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO messages (chat_id, user_id, role, content, provider_used)
                VALUES (?, ?, ?, ?, ?)
            """, (chat_id, user_id, role, content, provider_used))
            await db.commit()

    async def get_context(self, chat_id: int, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """Отримати останні повідомлення контексту для передачі в LLM."""
        lim = limit or settings.MAX_CONTEXT_MESSAGES
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                SELECT role, content FROM (
                    SELECT id, role, content FROM messages
                    WHERE chat_id = ?
                    ORDER BY id DESC
                    LIMIT ?
                ) ORDER BY id ASC
            """, (chat_id, lim))
            rows = await cursor.fetchall()
            return [{"role": r[0], "content": r[1]} for r in rows]

    async def clear_chat_context(self, chat_id: int) -> int:
        """Очистити контекст чату."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
            deleted = cursor.rowcount
            await db.commit()
            return deleted

    async def log_usage_stat(self, chat_id: int, user_id: Optional[int], provider: str, is_success: bool, error_message: Optional[str] = None):
        """Записати статистику виклику провайдера."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO usage_stats (chat_id, user_id, provider, is_success, error_message)
                VALUES (?, ?, ?, ?, ?)
            """, (chat_id, user_id, provider, 1 if is_success else 0, error_message))
            await db.commit()

    async def get_stats(self) -> Dict[str, Any]:
        """Отримати зведену статистику використання для адміна."""
        async with aiosqlite.connect(self.db_path) as db:
            # Загальна кількість повідомлень
            cursor = await db.execute("SELECT COUNT(*) FROM messages")
            total_msgs = (await cursor.fetchone())[0]

            # Кількість унікальних чатів
            cursor = await db.execute("SELECT COUNT(DISTINCT chat_id) FROM messages")
            total_chats = (await cursor.fetchone())[0]

            # Статистика по провайдерах
            cursor = await db.execute("""
                SELECT provider,
                       COUNT(*) as total_calls,
                       SUM(CASE WHEN is_success = 1 THEN 1 ELSE 0 END) as success_calls,
                       SUM(CASE WHEN is_success = 0 THEN 1 ELSE 0 END) as fail_calls
                FROM usage_stats
                GROUP BY provider
            """)
            provider_stats = await cursor.fetchall()

            return {
                "total_messages": total_msgs,
                "total_chats": total_chats,
                "provider_stats": [
                    {
                        "provider": r[0],
                        "total": r[1],
                        "success": r[2],
                        "failed": r[3],
                        "success_rate": f"{(r[2] / r[1] * 100):.1f}%" if r[1] > 0 else "0%"
                    }
                    for r in provider_stats
                ]
            }

    async def get_all_chats(self) -> List[int]:
        """Отримати список усіх унікальних chat_id."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT DISTINCT chat_id FROM chat_settings")
            rows = await cursor.fetchall()
            return [r[0] for r in rows]

memory = MemoryManager()
