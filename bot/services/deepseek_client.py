import logging
from typing import List, Dict, Optional
from openai import AsyncOpenAI
from bot.config import settings
from bot.services.key_pool import key_pool

logger = logging.getLogger(__name__)

class DeepSeekClient:
    def __init__(self):
        pass

    @property
    def is_available(self) -> bool:
        return key_pool.has_available_keys("deepseek")

    async def generate_response(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        model: str = "deepseek-chat",
        temperature: Optional[float] = None
    ) -> str:
        if not self.is_available:
            raise RuntimeError("DeepSeek API key is not configured or invalid.")

        api_key = key_pool.get_working_key("deepseek")
        if not api_key:
            raise RuntimeError("All DeepSeek keys are on cooldown or exhausted.")

        temp = temperature if temperature is not None else settings.TEMPERATURE
        payload_messages = [{"role": "system", "content": system_prompt}]
        for msg in messages:
            payload_messages.append({"role": msg["role"], "content": msg["content"]})

        client = AsyncOpenAI(api_key=api_key, base_url="https://api.deepseek.com", timeout=25.0)
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=payload_messages,
                temperature=temp,
                max_tokens=4000,
            )
            content = response.choices[0].message.content
            return content.strip() if content else ""
        except Exception as e:
            err_str = str(e)
            if "Insufficient Balance" in err_str or "402" in err_str:
                key_pool.mark_dead("deepseek", api_key, reason="Insufficient balance")
            elif "429" in err_str:
                key_pool.mark_rate_limited("deepseek", api_key, cooldown_seconds=60)
            logger.error(f"[DeepSeek] Error: {e}")
            raise e

    async def check_health(self) -> bool:
        if not self.is_available:
            return False
        try:
            res = await self.generate_response(
                system_prompt="Відповідай коротко: ОК.",
                messages=[{"role": "user", "content": "ping"}],
                model="deepseek-chat"
            )
            return bool(res)
        except Exception as e:
            return False

deepseek_service = DeepSeekClient()
