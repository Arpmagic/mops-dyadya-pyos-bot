import logging
from typing import List, Dict, Optional
from anthropic import AsyncAnthropic
from bot.config import settings
from bot.services.key_pool import key_pool

logger = logging.getLogger(__name__)

class AnthropicClient:
    def __init__(self):
        pass

    @property
    def is_available(self) -> bool:
        return key_pool.has_available_keys("anthropic")

    async def generate_response(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        model: str = "claude-3-5-haiku-20241022",
        temperature: Optional[float] = None
    ) -> str:
        if not self.is_available:
            raise RuntimeError("Anthropic API key is not configured or invalid.")

        api_key = key_pool.get_working_key("anthropic")
        if not api_key:
            raise RuntimeError("All Anthropic keys are on cooldown or exhausted.")

        claude_messages = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "assistant"
            if msg["content"].strip():
                claude_messages.append({"role": role, "content": msg["content"]})

        if not claude_messages:
            claude_messages = [{"role": "user", "content": "Привіт!"}]

        client = AsyncAnthropic(api_key=api_key, timeout=25.0)
        try:
            response = await client.messages.create(
                model=model,
                system=system_prompt,
                messages=claude_messages,
                max_tokens=2000,
            )
            text_blocks = [b.text for b in response.content if hasattr(b, "text")]
            return "".join(text_blocks).strip()
        except Exception as e:
            err_str = str(e)
            if "credit balance is too low" in err_str or "400" in err_str:
                key_pool.mark_dead("anthropic", api_key, reason="Low credit balance")
            elif "429" in err_str:
                key_pool.mark_rate_limited("anthropic", api_key, cooldown_seconds=60)
            logger.error(f"[Anthropic] Error: {e}")
            raise e

    async def check_health(self) -> bool:
        if not self.is_available:
            return False
        try:
            res = await self.generate_response(
                system_prompt="Відповідай коротко: ОК.",
                messages=[{"role": "user", "content": "ping"}],
                model="claude-3-5-haiku-20241022"
            )
            return bool(res)
        except Exception as e:
            return False

anthropic_service = AnthropicClient()
