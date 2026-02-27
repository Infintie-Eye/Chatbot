"""
Stage 4 — Output Stage.
Formats the AI response, saves to memory, and builds the final output dict.
"""
import uuid
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def run(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Output Stage: persist messages to memory and return the final API result.

    Reads from context:
        - message (str)            — user message
        - ai_response (str)        — model response
        - session_id (str)
        - model_used (str)
        - ai_latency_ms (float)
        - _stages (list)

    Writes to context:
        - result (dict)            — final API response payload
    """
    from src.core.memory_manager import memory_manager
    from src.core.session_manager import session_manager

    session_id = context["session_id"]
    user_message = context["message"]
    ai_response = context["ai_response"]
    model_used = context.get("model_used", "gemini-2.0-flash-exp")
    latency = context.get("ai_latency_ms", 0)

    # Persist both turns to memory
    memory_manager.add_message(session_id, "user", user_message)
    memory_manager.add_message(session_id, "assistant", ai_response)

    # Update session metadata
    session_manager.touch(session_id)

    message_id = str(uuid.uuid4())

    result = {
        "response": ai_response,
        "session_id": session_id,
        "message_id": message_id,
        "model": model_used,
        "ai_latency_ms": latency,
        "pipeline_stages": context.get("_stages", []) + ["output"],
        "context_info": context.get("context_summary", {}),
        "input_metadata": context.get("input_metadata", {}),
    }

    context.update({
        "result": result,
        "_stages": context.get("_stages", []) + ["output"],
    })

    logger.debug(
        f"[output] session={session_id} msg_id={message_id[:8]} "
        f"response_len={len(ai_response)}"
    )

    return context
