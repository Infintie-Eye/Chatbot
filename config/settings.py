"""
Configuration settings for the Blacifer Chatbot application.
"""
import os
from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""

    # API Keys
    gemini_api_key: Optional[str] = Field(
        default=None,
        env="GEMINI_API_KEY",
        description="Google Gemini API key"
    )

    # App Configuration
    app_name: str = Field(default="Blacifer Chatbot", description="Application name")
    app_version: str = Field(default="2.0.0", description="Application version")
    company_name: str = Field(default="Blacifer", description="Company name")

    # Model Configuration
    text_model: str = Field(default="gemini-2.0-flash-exp", description="Gemini text model")
    vision_model: str = Field(default="gemini-2.0-flash-exp", description="Gemini vision model")
    max_tokens: int = Field(default=8192, description="Maximum tokens for response")
    temperature: float = Field(default=0.7, description="Model temperature")

    # File Processing
    max_file_size_mb: int = Field(default=20, description="Maximum file size in MB")
    supported_text_formats: list = Field(
        default=["txt", "csv", "json", "pdf", "docx", "xlsx"],
        description="Supported text file formats"
    )
    supported_image_formats: list = Field(
        default=["jpg", "jpeg", "png", "gif", "bmp", "webp"],
        description="Supported image formats"
    )

    # UI Configuration
    page_title: str = Field(default="Conrux - AI Assistant", description="Page title")
    page_icon: str = Field(default="🤖", description="Page icon")
    layout: str = Field(default="wide", description="Streamlit layout")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str = Field(default="logs/app.log", description="Log file path")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()


# Validation
def validate_settings():
    """Validate required settings."""
    if not settings.gemini_api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is required. "
            "Please set it in your .env file or environment variables."
        )
    return True
