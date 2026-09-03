import logging
import asyncio
from typing import List, Dict, Optional
import httpx
from bot.config import settings
from bot.services.key_pool import key_pool

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.default_models = [
            "gemini-3.5-flash",
            "gemini-3.5-flash-lite",
            "gemini-3.1-flash-lite",
            "gemini-flash-lite-latest",
            "gemini-3-flash-preview"
        ]

    @property
    def is_available(self) -> bool:
        return key_pool.has_available_keys("gemini")

    async def generate_response(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        model: str = "gemini-3.6-flash",
        temperature: Optional[float] = None
    ) -> str:
        if not self.is_available:
            raise RuntimeError("Gemini API key is not configured or invalid.")

        temp = temperature if temperature is not None else settings.TEMPERATURE

        # Формування вмісту повідомлень
        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            parts = []
            if msg.get("content", "").strip():
                parts.append({"text": msg["content"]})
            if msg.get("image_base64"):
                imgs = msg["image_base64"]
                if isinstance(imgs, str):
                    imgs = [imgs]
                for img_b64 in imgs:
                    parts.append({
                        "inlineData": {
                            "mimeType": "image/jpeg",
                            "data": img_b64
                        }
                    })
            if parts:
                contents.append({
                    "role": role,
                    "parts": parts
                })

        if not contents:
            contents = [{"role": "user", "parts": [{"text": "Привіт!"}]}]

        payload = {
            "contents": contents,
            "system_instruction": {
                "parts": [{"text": system_prompt}]
            },
            "generationConfig": {
                "temperature": temp,
                "topP": 0.95,
                "maxOutputTokens": 4000
            },
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_CIVIC_INTEGRITY", "threshold": "BLOCK_NONE"}
            ]
        }

        models_to_try = [model] + [m for m in self.default_models if m != model]

        async with httpx.AsyncClient(timeout=25.0) as client:
            last_err = None
            api_key = key_pool.get_working_key("gemini")
            if not api_key:
                raise RuntimeError("No Gemini API key available.")

            for m in models_to_try:
                url = f"{self.base_url}/{m}:generateContent?key={api_key}"
                try:
                    resp = await client.post(url, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            parts = candidates[0].get("content", {}).get("parts", [])
                            text_pieces = [p.get("text", "") for p in parts if "text" in p]
                            full_text = "".join(text_pieces).strip()
                            if full_text:
                                return full_text
                    elif resp.status_code == 429:
                        # Модель перевантажена, пробуємо наступну модель негайно!
                        logger.warning(f"[Gemini] Модель {m} повернула 429. Миттєво перемикаємось на наступну модель...")
                        last_err = f"429 Rate limit on {m}"
                        continue
                    elif resp.status_code in [400, 403]:
                        err_msg = resp.text[:150]
                        if "API_KEY_INVALID" in err_msg or "PERMISSION_DENIED" in err_msg:
                            key_pool.mark_dead("gemini", api_key, reason=err_msg)
                        last_err = err_msg
                        continue
                    else:
                        last_err = f"Status {resp.status_code}: {resp.text[:150]}"
                        continue
                except Exception as e:
                    last_err = e
                    continue

            raise RuntimeError(f"Gemini generation failed on all models. Last error: {last_err}")

    async def check_health(self) -> bool:
        if not self.is_available:
            return False
        try:
            res = await self.generate_response(
                system_prompt="Відповідай коротко: ОК.",
                messages=[{"role": "user", "content": "ping"}],
                model="gemini-3.6-flash"
            )
            return bool(res)
        except Exception as e:
            return False

gemini_service = GeminiClient()
