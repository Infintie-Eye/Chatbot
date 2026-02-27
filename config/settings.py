"""
Configuration settings for the Expert Chatbot.
Supports all features: FastAPI, Gemini AI, Pipeline, Sessions.
"""
import os
from typing import Optional, List
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

load_dotenv()


class Settings(BaseSettings):
    """Application settings — loaded from .env."""

    # ── API Keys ────────────────────────────────────────────────────────
    gemini_api_key: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    chatbot_api_key: Optional[str] = Field(default=None, env="CHATBOT_API_KEY")

    # ── App Identity ─────────────────────────────────────────────────────
    app_name: str = Field(default="Conrux AI", env="APP_NAME")
    app_version: str = Field(default="3.0.0", env="APP_VERSION")
    company_name: str = Field(default="Blacifer", env="COMPANY_NAME")

    # ── FastAPI Server ────────────────────────────────────────────────────
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_prefix: str = Field(default="/api/v1", env="API_PREFIX")
    debug: bool = Field(default=False, env="DEBUG")
    allowed_origins: List[str] = Field(
        default=["http://localhost:8501", "http://127.0.0.1:8501", "*"],
        env="ALLOWED_ORIGINS"
    )

    # ── Gemini Model ──────────────────────────────────────────────────────
    text_model: str = Field(default="models/gemini-2.5-flash-lite", env="TEXT_MODEL")
    vision_model: str = Field(default="models/gemini-2.5-flash-lite", env="VISION_MODEL")
    max_tokens: int = Field(default=2048, env="MAX_TOKENS")
    temperature: float = Field(default=0.7, env="TEMPERATURE")
    top_p: float = Field(default=0.95, env="TOP_P")
    top_k: int = Field(default=40, env="TOP_K")

    # ── Pipeline ──────────────────────────────────────────────────────────
    max_context_messages: int = Field(default=20, env="MAX_CONTEXT_MESSAGES")
    max_input_length: int = Field(default=10000, env="MAX_INPUT_LENGTH")
    stream_enabled: bool = Field(default=True, env="STREAM_ENABLED")

    # ── Session / Memory ─────────────────────────────────────────────────
    session_ttl_seconds: int = Field(default=3600, env="SESSION_TTL_SECONDS")
    max_sessions: int = Field(default=1000, env="MAX_SESSIONS")

    # ── Rate Limiting ─────────────────────────────────────────────────────
    rate_limit_chat: str = Field(default="30/minute", env="RATE_LIMIT_CHAT")
    rate_limit_analysis: str = Field(default="10/minute", env="RATE_LIMIT_ANALYSIS")

    # ── File Processing ───────────────────────────────────────────────────
    max_file_size_mb: int = Field(default=20, env="MAX_FILE_SIZE_MB")
    supported_text_formats: list = Field(
        default=["txt", "csv", "json", "pdf", "docx", "xlsx", "md"]
    )
    supported_image_formats: list = Field(
        default=["jpg", "jpeg", "png", "gif", "bmp", "webp"]
    )

    # ── Streamlit UI ──────────────────────────────────────────────────────
    page_title: str = Field(default="Conrux AI — Expert Chatbot", env="PAGE_TITLE")
    page_icon: str = Field(default="✦", env="PAGE_ICON")
    layout: str = Field(default="wide", env="LAYOUT")

    # ── Logging ───────────────────────────────────────────────────────────
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/app.log", env="LOG_FILE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()


def validate_settings():
    """Validate that required settings are present."""
    if not settings.gemini_api_key:
        raise ValueError(
            "GEMINI_API_KEY is required. Add it to your .env file."
        )
    return True
