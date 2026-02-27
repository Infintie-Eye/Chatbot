"""
Chat router — text conversation endpoints.
POST /api/v1/chat              — Send a message (returns full response)
POST /api/v1/chat/session      — Create a new session
GET  /api/v1/chat/history/{id} — Retrieve conversation history
DELETE /api/v1/chat/history/{id} — Clear a session's history
"""
import uuid
import time
import logging
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import StreamingResponse

from api.models.schemas import (
    ChatRequest, ChatResponse, SessionCreate,
    ConversationHistory, APIResponse
)
from src.pipeline.pipeline_manager import PipelineManager

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Chat"])
pipeline = PipelineManager()


@router.post(
    "/chat",
    response_model=APIResponse,
    summary="Send a chat message",
    description="Send a message to the AI. Optionally provide a session_id for multi-turn conversation."
)
async def chat(request: Request, body: ChatRequest):
    """Process a chat message through the full pipeline."""
    start = time.perf_counter()

    # Auto-create a session if not provided
    session_id = body.session_id or str(uuid.uuid4())

    try:
        result = await pipeline.run_chat(
            message=body.message,
            session_id=session_id,
            system_prompt=body.system_prompt,
            temperature=body.temperature,
        )

        latency = (time.perf_counter() - start) * 1000
        result["latency_ms"] = round(latency, 2)
        result["session_id"] = session_id

        return APIResponse(
            success=True,
            data=result,
            metadata={
                "request_id": getattr(request.state, "request_id", "n/a"),
                "latency_ms": round(latency, 2),
            }
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        logger.error(f"Chat pipeline error: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/chat/session",
    response_model=APIResponse,
    summary="Create a new chat session",
    description="Create a new conversation session and return its ID."
)
async def create_session():
    """Create a new conversation session."""
    from src.core.session_manager import session_manager
    from datetime import datetime

    session_id = str(uuid.uuid4())
    session_manager.create_session(session_id)

    return APIResponse(
        success=True,
        data={
            "session_id": session_id,
            "created_at": datetime.utcnow().isoformat(),
            "message": "Session created. Use this session_id in subsequent /chat requests."
        }
    )


@router.get(
    "/chat/history/{session_id}",
    response_model=APIResponse,
    summary="Get conversation history",
    description="Retrieve the full conversation history for a session."
)
async def get_history(session_id: str):
    """Get conversation history for a session."""
    from src.core.memory_manager import memory_manager

    history = memory_manager.get_history(session_id)
    if history is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session '{session_id}' not found or expired."
        )

    return APIResponse(
        success=True,
        data={
            "session_id": session_id,
            "messages": [m.model_dump() for m in history],
            "message_count": len(history),
        }
    )


@router.delete(
    "/chat/history/{session_id}",
    response_model=APIResponse,
    summary="Clear conversation history",
    description="Delete all messages in a session's conversation history."
)
async def clear_history(session_id: str):
    """Clear conversation history for a session."""
    from src.core.memory_manager import memory_manager
    from src.core.session_manager import session_manager

    memory_manager.clear(session_id)
    session_manager.reset(session_id)

    return APIResponse(
        success=True,
        data={"session_id": session_id, "message": "Conversation history cleared."}
    )
