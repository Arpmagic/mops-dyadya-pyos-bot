import json
import logging
import math
import httpx
from bot.config import settings

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.db = []
        self.api_key = settings.GEMINI_API_KEY
        self.model = "models/gemini-embedding-2"
        self.url = f"https://generativelanguage.googleapis.com/v1beta/{self.model}:embedContent?key={self.api_key}"
        self.load_db()

    def load_db(self):
        try:
            import os
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "rag_database.json")
            with open(db_path, "r", encoding="utf-8") as f:
                self.db = json.load(f)
            logger.info(f"[RAG] Successfully loaded {len(self.db)} lore chunks.")
        except Exception as e:
            logger.error(f"[RAG] Failed to load rag_database.json: {e}")
            self.db = []

    async def get_embedding(self, text: str) -> list[float]:
        try:
            async with httpx.AsyncClient() as client:
                data = {
                    "model": self.model,
                    "content": {"parts": [{"text": text}]}
                }
                response = await client.post(self.url, json=data)
                response.raise_for_status()
                res_data = response.json()
                return res_data["embedding"]["values"]
        except Exception as e:
            logger.error(f"[RAG] Failed to get embedding for query: {e}")
            return []

    def cosine_similarity(self, v1: list[float], v2: list[float]) -> float:
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm_v1 = math.sqrt(sum(a * a for a in v1))
        norm_v2 = math.sqrt(sum(b * b for b in v2))
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0
        return dot_product / (norm_v1 * norm_v2)

    async def get_relevant_lore(self, query: str, top_k: int = 2) -> str:
        if not self.db:
            return ""
            
        query_emb = await self.get_embedding(query)
        if not query_emb:
            return ""

        scored_chunks = []
        for item in self.db:
            score = self.cosine_similarity(query_emb, item["embedding"])
            scored_chunks.append((score, item["text"]))

        # Sort by score descending
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        # Only take top_k chunks, and only if score is reasonably high (e.g., > 0.5)
        best_chunks = [chunk for score, chunk in scored_chunks[:top_k] if score > 0.5]
        
        if not best_chunks:
            return ""
            
        return "\n\n---\n\n".join(best_chunks)

rag_service = RAGService()
