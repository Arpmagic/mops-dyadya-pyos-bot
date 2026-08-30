import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: str = ""
    ALLOWED_CHATS: str = ""

    OPENAI_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    DEFAULT_ROLE: str = "mops"
    DEFAULT_ROUTER_MODE: str = "auto"
    MAX_CONTEXT_MESSAGES: int = 15
    TEMPERATURE: float = 0.92
    DATABASE_PATH: str = "data/bot_database.sqlite"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def admin_id_list(self) -> List[int]:
        if not self.ADMIN_IDS:
            return []
        return [int(x.strip()) for x in self.ADMIN_IDS.split(",") if x.strip()]

    @property
    def allowed_chat_list(self) -> List[int]:
        if not self.ALLOWED_CHATS:
            return []
        return [int(x.strip()) for x in self.ALLOWED_CHATS.split(",") if x.strip()]

    @property
    def db_full_path(self) -> Path:
        p = Path(self.DATABASE_PATH)
        if not p.is_absolute():
            p = BASE_DIR / p
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

settings = Settings()
