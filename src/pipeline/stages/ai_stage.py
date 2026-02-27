"""
Stage 3 — AI Stage.
Sends the prepared prompt + history to Gemini and captures the response.
"""
import time
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def run(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    AI Stage: call Gemini with the user message + conversation history.

    Reads from context:
        - message (str)
        - history (list)           — Gemini-format history
        - system_instruction (str)
        - temperature (float, opt)

    Writes to context:
        - ai_response (str)        — raw model text
        - model_used (str)
        - ai_latency_ms (float)
    """
    from src.core.gemini_client import gemini_client
    from config.settings import settings

    message = context["message"]
    history = context.get("history", [])
    system_instruction = context.get("system_instruction")
    temperature = context.get("temperature")

    start = time.perf_counter()

    if history:
        response_text = gemini_client.generate_with_history(
            prompt=message,
            history=history,
            system_instruction=system_instruction,
            temperature=temperature,
        )
    else:
        response_text = gemini_client.generate_text_response(
            prompt=message,
            system_instruction=system_instruction,
            temperature=temperature,
        )

    elapsed_ms = (time.perf_counter() - start) * 1000

    logger.debug(
        f"[ai] session={context.get('session_id')} "
        f"latency={elapsed_ms:.1f}ms response_len={len(response_text)}"
    )

    context.update({
        "ai_response": response_text,
        "model_used": settings.text_model,
        "ai_latency_ms": round(elapsed_ms, 2),
        "_stages": context.get("_stages", []) + ["ai"],
    })

    return context
