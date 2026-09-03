import logging
from typing import List, Dict, Optional
from openai import AsyncOpenAI
from bot.config import settings
from bot.services.key_pool import key_pool

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        pass

    @property
    def is_available(self) -> bool:
        return key_pool.has_available_keys("openai")

    async def generate_response(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        temperature: Optional[float] = None
    ) -> str:
        if not self.is_available:
            raise RuntimeError("OpenAI API key is not configured or invalid.")

        api_key = key_pool.get_working_key("openai")
        if not api_key:
            raise RuntimeError("All OpenAI keys are on cooldown or exhausted.")

        temp = temperature if temperature is not None else settings.TEMPERATURE
        payload_messages = [{"role": "system", "content": system_prompt}]
        for msg in messages:
            payload_messages.append({"role": msg["role"], "content": msg["content"]})

        client = AsyncOpenAI(api_key=api_key, timeout=25.0)
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=payload_messages,
                temperature=temp,
                max_tokens=2000,
            )
            content = response.choices[0].message.content
            return content.strip() if content else ""
        except Exception as e:
            err_str = str(e)
            if "insufficient_quota" in err_str or "credit_balance_exhausted" in err_str:
                key_pool.mark_dead("openai", api_key, reason="No credits")
            elif "429" in err_str:
                key_pool.mark_rate_limited("openai", api_key, cooldown_seconds=60)
            logger.error(f"[OpenAI] Error: {e}")
            raise e

    async def check_health(self) -> bool:
        if not self.is_available:
            return False
        try:
            res = await self.generate_response(
                system_prompt="Відповідай коротко: ОК.",
                messages=[{"role": "user", "content": "ping"}],
                model="gpt-4o-mini"
            )
            return bool(res)
        except Exception as e:
            return False

openai_service = OpenAIClient()
