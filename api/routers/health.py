"""
Health & Info router.
GET /api/v1/health  — API status + Gemini connectivity
GET /api/v1/info    — Model info, capabilities, limits
"""
import time
import logging
import sys
from datetime import datetime
from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])

# Record startup time for uptime calculation
_start_time = time.time()


@router.get("/health", summary="Health check")
async def health_check():
    """Check API health and Gemini API connectivity."""
    from src.core.gemini_client import gemini_client
    from src.core.session_manager import session_manager
    from config.settings import settings

    gemini_status = "unknown"
    try:
        test = gemini_client.test_connection()
        gemini_status = "connected" if test["status"] == "success" else "error"
    except Exception as e:
        gemini_status = f"error: {str(e)[:60]}"

    return {
        "success": True,
        "data": {
            "status": "healthy",
            "version": settings.app_version,
            "app_name": settings.app_name,
            "gemini_status": gemini_status,
            "active_sessions": session_manager.count(),
            "uptime_seconds": round(time.time() - _start_time, 1),
            "timestamp": datetime.utcnow().isoformat(),
            "python_version": sys.version.split()[0],
        }
    }


@router.get("/info", summary="Model & configuration info")
async def model_info():
    """Return current model configuration and supported capabilities."""
    from config.settings import settings

    return {
        "success": True,
        "data": {
            "text_model": settings.text_model,
            "vision_model": settings.vision_model,
            "max_tokens": settings.max_tokens,
            "temperature": settings.temperature,
            "max_context_messages": settings.max_context_messages,
            "max_input_length": settings.max_input_length,
            "session_ttl_seconds": settings.session_ttl_seconds,
            "rate_limits": {
                "chat": settings.rate_limit_chat,
                "analysis": settings.rate_limit_analysis,
            },
            "supported_file_types": {
                "text": settings.supported_text_formats,
                "image": settings.supported_image_formats,
            },
            "features": [
                "multi_turn_conversation",
                "image_analysis",
                "document_processing",
                "session_memory",
                "streaming_ready",
            ]
        }
    }
