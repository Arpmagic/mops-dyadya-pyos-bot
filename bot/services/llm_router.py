import logging
import itertools
from typing import List, Dict, Tuple, Optional, Any
from bot.services.openai_client import openai_service
from bot.services.deepseek_client import deepseek_service
from bot.services.anthropic_client import anthropic_service
from bot.services.gemini_client import gemini_service
from bot.services.memory import memory
from bot.services.rag_service import rag_service

logger = logging.getLogger(__name__)

class LLMRoutesManager:
    def __init__(self):
        self.providers = {
            "gemini": {
                "service": gemini_service,
                "default_model": "gemini-3.5-flash",
                "display_name": "Google Gemini (Flash)",
            },
            "deepseek": {
                "service": deepseek_service,
                "default_model": "deepseek-chat",
                "display_name": "DeepSeek (V3/Chat)",
            },
            "openai": {
                "service": openai_service,
                "default_model": "gpt-4o-mini",
                "display_name": "OpenAI (GPT-4o mini)",
            },
            "anthropic": {
                "service": anthropic_service,
                "default_model": "claude-3-5-haiku-20241022",
                "display_name": "Claude 3.5 Haiku",
            }
        }
        self._provider_cycle = itertools.cycle(["gemini", "deepseek", "openai", "anthropic"])

    def get_available_providers(self) -> List[str]:
        """Список доступних провайдерів з хоча б одним не заблокованим ключем."""
        return [
            name for name, info in self.providers.items()
            if info["service"].is_available
        ]

    async def generate_response(
        self,
        chat_id: int,
        user_id: Optional[int],
        system_prompt: str,
        messages: List[Dict[str, str]],
        mode: str = "auto",
    ) -> Tuple[str, str, str]:
        """
        Генерує відповідь з автоматичним пулом ключів та Fallback.
        """
        available = self.get_available_providers()
        if not available:
            # Якщо всі позначені як dead, скидаємо стан і пробуємо Gemini
            available = ["gemini"]

        attempts_order = []
        if mode in self.providers and mode in available:
            attempts_order = [mode] + [p for p in available if p != mode]
        else:
            # Завжди надаємо пріоритет робочому провайдеру (Gemini)
            if "gemini" in available:
                attempts_order = ["gemini"] + [p for p in available if p != "gemini"]
            else:
                attempts_order = available

        # --- RAG INTEGRATION ---
        last_user_msg = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        if last_user_msg:
            try:
                retrieved_lore = await rag_service.get_relevant_lore(last_user_msg)
                if retrieved_lore:
                    system_prompt += "\n\n[ДИНАМИЧЕСКАЯ СПРАВКА ИЗ ЭНЦИКЛОПЕДИИ ЛОРА (ДЛЯ КОНТЕКСТА)]\n" + retrieved_lore + "\n[КОНЕЦ СПРАВКИ. ИСПОЛЬЗУЙ ЭТИ ДАННЫЕ ДЛЯ ОТВЕТА, ЕСЛИ ОНИ ПОДХОДЯТ.]"
            except Exception as e:
                logger.error(f"[RAG] Error during retrieval: {e}")
        # -----------------------

        last_error = None
        for provider_name in attempts_order:
            provider_info = self.providers.get(provider_name)
            if not provider_info:
                continue

            service = provider_info["service"]
            model = provider_info["default_model"]

            try:
                response_text = await service.generate_response(
                    system_prompt=system_prompt,
                    messages=messages,
                    model=model
                )

                if response_text:
                    import re
                    # Remove <thinking>...</thinking> and <thought>...</thought> tags and their contents (case-insensitive)
                    # Strip closed XML tags
                    cleaned_text = re.sub(r'<([a-zA-Z0-9_-]+)>.*?</\1>', '', response_text, flags=re.DOTALL | re.IGNORECASE)
                    # Strip unclosed XML tags that reach the end of the text
                    cleaned_text = re.sub(r'<([a-zA-Z0-9_-]+)>.*$', '', cleaned_text, flags=re.DOTALL | re.IGNORECASE)
                    cleaned_text = cleaned_text.strip()
                    cleaned_text = re.sub(r'<[Tt]hought>.*?</[Tt]hought>', '', cleaned_text, flags=re.DOTALL | re.IGNORECASE)
                    cleaned_text = re.sub(r'<[Tt]houghts>.*?</[Tt]houghts>', '', cleaned_text, flags=re.DOTALL | re.IGNORECASE)
                    # Sometimes the LLM fails to close the tag or uses formatting like ```<thinking>
                    cleaned_text = re.sub(r'```.*?<thinking>.*?</thinking>.*?```', '', cleaned_text, flags=re.DOTALL | re.IGNORECASE)
                    
                    # Also sometimes they just write "Thinking process:" or "Thoughts:" without tags if the instruction wasn't strict enough
                    # but since we strictly instruct tags, we just remove the tags.
                    cleaned_text = cleaned_text.strip()
                    
                    # If cleaned_text is empty, it means the model ONLY output thoughts and got cut off or failed to write the answer.
                    if not cleaned_text:
                        raise ValueError("Model hit max_tokens mid-thought or failed to provide a final response.")
                        
                    await memory.log_usage_stat(
                        chat_id=chat_id,
                        user_id=user_id,
                        provider=provider_name,
                        is_success=True
                    )
                    return cleaned_text, provider_name, model

            except Exception as e:
                logger.warning(f"[{provider_name.upper()}] Помилка: {e}. Перемикаємось на наступний...")
                await memory.log_usage_stat(
                    chat_id=chat_id,
                    user_id=user_id,
                    provider=provider_name,
                    is_success=False,
                    error_message=str(e)[:250]
                )
                last_error = e
                continue

        error_msg = f"Усі AI-провайдери повернули помилки. Остання: {last_error}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    async def check_all_keys(self) -> Dict[str, Dict[str, Any]]:
        results = {}
        for name, info in self.providers.items():
            service = info["service"]
            if not service.is_available:
                results[name] = {
                    "display_name": info["display_name"],
                    "status": "❌ Немає активних ключів / вичерпано",
                    "ok": False
                }
                continue

            try:
                is_ok = await service.check_health()
                results[name] = {
                    "display_name": info["display_name"],
                    "status": "✅ Працює (OK)" if is_ok else "⚠️ Помилка лімітів/балансу",
                    "ok": is_ok
                }
            except Exception as e:
                results[name] = {
                    "display_name": info["display_name"],
                    "status": f"❌ {str(e)[:60]}",
                    "ok": False
                }

        return results

llm_router = LLMRoutesManager()
