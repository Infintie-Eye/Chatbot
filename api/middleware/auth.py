"""
API Key authentication middleware.
Validates X-API-Key header against CHATBOT_API_KEY from settings.
If CHATBOT_API_KEY is not set, auth is disabled (open access).
"""
import logging
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from config.settings import settings

logger = logging.getLogger(__name__)

# Paths that bypass auth entirely
PUBLIC_PATHS = {"/", "/docs", "/redoc", "/openapi.json", "/api/v1/health", "/api/v1/info"}


class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    """Optional API key authentication middleware."""

    async def dispatch(self, request: Request, call_next):
        # Skip auth if no key is configured
        if not settings.chatbot_api_key:
            return await call_next(request)

        # Skip auth for public paths
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        # Validate the key
        api_key = request.headers.get("X-API-Key") or request.query_params.get("api_key")
        if not api_key or api_key != settings.chatbot_api_key:
            logger.warning(f"Unauthorized request to {request.url.path} from {request.client.host}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "success": False,
                    "error": "Invalid or missing API key",
                    "detail": "Provide your API key via the X-API-Key header"
                }
            )

        return await call_next(request)
