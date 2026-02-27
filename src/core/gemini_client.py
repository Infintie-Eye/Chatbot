"""
Gemini Client — uses the battle-tested legacy google.generativeai SDK.
Fully supports gemini-1.5-flash on the free tier.
FutureWarning is suppressed intentionally; migration to google.genai requires
Gemini billing enabled, which is incompatible with free-tier API keys.
"""
import logging
import io
import warnings
from typing import Dict, List, Any, Optional
from PIL import Image
from tenacity import retry, stop_after_attempt, wait_exponential

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.settings import settings

logger = logging.getLogger(__name__)

# Suppress FutureWarning from google.generativeai (intentional — new SDK blocks free tier)
warnings.filterwarnings("ignore", category=FutureWarning, module="google")

import google.generativeai as genai
genai.configure(api_key=settings.gemini_api_key)


class GeminiClient:
    """
    Gemini 1.5 Flash client using the legacy google.generativeai SDK.
    Works with free-tier API keys (15 RPM, 1M tokens/day).
    """

    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required.")
        logger.info(f"GeminiClient ready | model: {settings.text_model} | sdk: google.generativeai")

    def _gen_config(self, temperature: Optional[float] = None):
        return genai.types.GenerationConfig(
            temperature=temperature if temperature is not None else settings.temperature,
            max_output_tokens=settings.max_tokens,
            top_p=settings.top_p,
            top_k=settings.top_k,
        )

    # ══════════════  TEXT — SINGLE TURN  ══════════════

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10), reraise=True)
    def generate_text_response(
        self,
        prompt: str,
        context: Optional[str] = None,
        system_instruction: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> str:
        parts = []
        if context:
            parts.append(f"Context:\n{context}\n")
        parts.append(prompt)
        full_prompt = "\n\n".join(parts)

        model = genai.GenerativeModel(
            settings.text_model,
            system_instruction=system_instruction,
        )
        resp = model.generate_content(full_prompt, generation_config=self._gen_config(temperature))
        return self._extract(resp)

    # ══════════════  TEXT — MULTI TURN  ══════════════

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10), reraise=True)
    def generate_with_history(
        self,
        prompt: str,
        history: List[Dict[str, str]],
        system_instruction: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> str:
        model = genai.GenerativeModel(
            settings.text_model,
            system_instruction=system_instruction,
        )
        chat = model.start_chat(history=history or [])
        resp = chat.send_message(prompt, generation_config=self._gen_config(temperature))
        return self._extract(resp)

    # ══════════════  IMAGE ANALYSIS  ══════════════

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10), reraise=True)
    def analyze_image(
        self,
        image: Image.Image,
        prompt: str,
        system_instruction: Optional[str] = None,
    ) -> str:
        model = genai.GenerativeModel(
            settings.vision_model,
            system_instruction=system_instruction,
        )
        resp = model.generate_content(
            [prompt, image],
            generation_config=self._gen_config(),
        )
        return self._extract(resp)

    # ══════════════  DOCUMENT ANALYSIS  ══════════════

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10), reraise=True)
    def process_document(
        self,
        content: str,
        query: str,
        file_type: str,
        system_instruction: Optional[str] = None,
    ) -> str:
        # Cap content to stay within token limits
        prompt = (
            f"Document Type: {file_type.upper()}\n\n"
            f"Document Content:\n```\n{content[:6000]}\n```\n\n"
            f"User Query: {query}\n\n"
            "Provide a comprehensive, accurate response based only on the document."
        )
        model = genai.GenerativeModel(
            settings.text_model,
            system_instruction=system_instruction,
        )
        resp = model.generate_content(prompt, generation_config=self._gen_config())
        return self._extract(resp)

    # ══════════════  UTILITIES  ══════════════

    def test_connection(self) -> Dict[str, Any]:
        """Quick connectivity test — returns status dict."""
        try:
            result = self.generate_text_response("Reply with the word: OK")
            return {"status": "connected", "response_preview": result[:80]}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_model_info(self) -> Dict[str, Any]:
        return {
            "current_model": settings.text_model,
            "sdk": "google.generativeai (legacy)",
            "api_key_set": bool(settings.gemini_api_key),
        }

    @staticmethod
    def _extract(response) -> str:
        """Safely extract text from a GenerateResponse."""
        try:
            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text
        except Exception:
            pass
        try:
            return response.text
        except Exception:
            return "I'm sorry, I couldn't generate a response. Please try again."


# ── Singleton ──────────────────────────────────────────────────────────────────
gemini_client = GeminiClient()
