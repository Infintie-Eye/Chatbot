"""
Stage 2 — Context Stage.
Loads conversation history from memory and builds the context window for the AI.
"""
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Default system persona
DEFAULT_SYSTEM_PROMPT = """You are Conrux, an elite AI assistant created by Blacifer, powered by Google Gemini 2.0 Flash.
You are sophisticated, knowledgeable, and articulate. You provide thoughtful, accurate, and deeply helpful responses.
Maintain a professional yet warm tone. Format longer responses with markdown for clarity.
You remember the conversation history and build context across messages."""


def run(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Context Stage: load conversation history and prepare the AI context.

    Reads from context:
        - session_id (str)
        - system_prompt (str, optional) — custom override

    Writes to context:
        - history (list)         — Gemini-format chat history
        - system_instruction (str)
        - context_summary (dict) — message count, window size
    """
    from src.core.memory_manager import memory_manager
    from config.settings import settings

    session_id = context["session_id"]
    system_instruction = context.get("system_prompt") or DEFAULT_SYSTEM_PROMPT

    # Load history in Gemini format
    history = memory_manager.get_gemini_history(
        session_id,
        last_n=settings.max_context_messages
    )

    message_count = len(history)
    logger.debug(f"[context] session={session_id} history_msgs={message_count}")

    context.update({
        "history": history,
        "system_instruction": system_instruction,
        "context_summary": {
            "history_message_count": message_count,
            "context_window_limit": settings.max_context_messages,
        },
        "_stages": context.get("_stages", []) + ["context"],
    })

    return context
