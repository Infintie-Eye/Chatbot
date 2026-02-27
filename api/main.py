"""
FastAPI Application Entry Point — Conrux AI Expert Chatbot.

Mounts:
  /api/v1/health   — health & info
  /api/v1/chat     — conversation endpoints
  /api/v1/analyze  — image & document endpoints
  /                — serves the luxury HTML frontend
"""
import logging
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# ── Project root on path ─────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent   # project root (parent of api/)
sys.path.insert(0, str(ROOT))

from config.settings import settings
from api.middleware.auth import APIKeyAuthMiddleware
from api.middleware.logging_middleware import LoggingMiddleware
from api.routers import health, chat, images, documents
from src.core.memory_manager import memory_manager
from src.core.session_manager import session_manager

# ── Logging setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)


# ── App factory ──────────────────────────────────────────────────────────────
def create_app() -> FastAPI:
    app = FastAPI(
        title=f"{settings.app_name} API",
        description=(
            "Expert AI Chatbot powered by Google Gemini 2.0 Flash. "
            "Supports multi-turn conversation, image analysis, and document processing."
        ),
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # ── Middleware (order matters: outermost added last) ────────────────
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(APIKeyAuthMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Routers ──────────────────────────────────────────────────────────
    prefix = settings.api_prefix
    app.include_router(health.router,    prefix=prefix)
    app.include_router(chat.router,      prefix=prefix)
    app.include_router(images.router,    prefix=prefix)
    app.include_router(documents.router, prefix=prefix)

    # ── Static frontend ──────────────────────────────────────────────────
    frontend_dir = ROOT / "frontend"
    if frontend_dir.exists():
        app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

        @app.get("/", include_in_schema=False)
        async def serve_frontend():
            return FileResponse(str(frontend_dir / "index.html"))

    # ── Startup / Shutdown ────────────────────────────────────────────────
    @app.on_event("startup")
    async def on_startup():
        memory_manager.configure(
            ttl=settings.session_ttl_seconds,
            max_messages=settings.max_context_messages * 2
        )
        session_manager.configure(ttl=settings.session_ttl_seconds)
        logger.info(
            f"✦ {settings.app_name} v{settings.app_version} started "
            f"on {settings.api_host}:{settings.api_port}"
        )

    @app.on_event("shutdown")
    async def on_shutdown():
        evicted = session_manager.evict_expired()
        logger.info(f"✦ Shutdown complete. Evicted {evicted} expired sessions.")

    return app


app = create_app()


# ── Run directly ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
