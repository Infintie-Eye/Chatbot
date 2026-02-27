"""
Structured request/response logging middleware.
Logs method, path, status code, and processing time for every request.
"""
import time
import logging
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("api.access")


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log every incoming request with timing information."""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        start_time = time.perf_counter()

        # Attach request ID to state for downstream use
        request.state.request_id = request_id

        logger.info(
            f"[{request_id}] → {request.method} {request.url.path} "
            f"| client={request.client.host if request.client else 'unknown'}"
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            elapsed = (time.perf_counter() - start_time) * 1000
            logger.error(
                f"[{request_id}] ✗ {request.method} {request.url.path} "
                f"| ERROR={type(exc).__name__} | {elapsed:.1f}ms"
            )
            raise

        elapsed = (time.perf_counter() - start_time) * 1000
        status = response.status_code
        level = logging.INFO if status < 400 else logging.WARNING if status < 500 else logging.ERROR
        logger.log(
            level,
            f"[{request_id}] ← {request.method} {request.url.path} "
            f"| {status} | {elapsed:.1f}ms"
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-Ms"] = f"{elapsed:.1f}"
        return response
