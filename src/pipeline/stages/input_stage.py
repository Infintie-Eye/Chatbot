"""
Stage 1 — Input Stage.
Validates, sanitizes, and enriches the raw user input before it enters the pipeline.
"""
import re
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Patterns that look like prompt injections or abuse
_INJECTION_PATTERNS = [
    r"ignore\s+(?:all\s+)?(?:previous|above)\s+instructions?",
    r"you\s+are\s+now\s+(?:a\s+)?(?:dan|jailbreak)",
    r"disregard\s+(?:all\s+)?(?:your\s+)?(?:instructions?|training)",
]
_INJECTION_RE = re.compile("|".join(_INJECTION_PATTERNS), re.IGNORECASE)


def run(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Input Stage: validate and prepare the user message.

    Reads from context:
        - raw_message (str)
        - session_id (str)

    Writes to context:
        - message (str)          — sanitized message
        - session_id (str)       — confirmed/created session ID
        - timestamp (str)        — UTC ISO timestamp
        - request_id (str)       — unique ID for this request
        - input_metadata (dict)  — character count, word count, language hint

    Raises:
        ValueError — if message is too long, empty, or flagged
    """
    from config.settings import settings

    raw = context.get("raw_message", "").strip()
    session_id = context.get("session_id") or str(uuid.uuid4())

    # ── Validators ──────────────────────────────────────────────────────
    if not raw:
        raise ValueError("Message cannot be empty.")

    if len(raw) > settings.max_input_length:
        raise ValueError(
            f"Message too long: {len(raw)} chars (max {settings.max_input_length})."
        )

    # Detect injection attempts
    if _INJECTION_RE.search(raw):
        logger.warning(f"[{session_id}] Potential prompt injection detected.")
        raise ValueError("Your message contains content that cannot be processed.")

    # ── Light sanitization ───────────────────────────────────────────────
    sanitized = raw[:settings.max_input_length]
    sanitized = re.sub(r"\s{3,}", "  ", sanitized)  # collapse excessive whitespace

    # ── Metadata ─────────────────────────────────────────────────────────
    word_count = len(sanitized.split())

    context.update({
        "message": sanitized,
        "session_id": session_id,
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": str(uuid.uuid4()),
        "input_metadata": {
            "char_count": len(sanitized),
            "word_count": word_count,
            "original_length": len(raw),
        },
        "_stages": context.get("_stages", []) + ["input"],
    })

    logger.debug(f"[input] session={session_id} words={word_count}")
    return context
