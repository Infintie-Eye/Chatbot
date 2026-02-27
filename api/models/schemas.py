"""Pydantic v2 schemas for all API request and response models."""
import uuid
from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field


# ══════════════════════════════════════════════════════════════════
#  SHARED
# ══════════════════════════════════════════════════════════════════

class APIResponse(BaseModel):
    """Standard API response envelope."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    error: str
    detail: Optional[str] = None
    code: Optional[int] = None


# ══════════════════════════════════════════════════════════════════
#  CHAT
# ══════════════════════════════════════════════════════════════════

class ChatRequest(BaseModel):
    """Single-turn chat request."""
    message: str = Field(..., min_length=1, max_length=10000, description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    system_prompt: Optional[str] = Field(None, description="Custom system instruction override")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0, description="Generation temperature")
    stream: bool = Field(False, description="Enable streaming response")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Explain quantum computing in simple terms.",
                "session_id": "sess_abc123",
                "stream": False
            }
        }


class Message(BaseModel):
    """A single conversation message."""
    role: str = Field(..., description="'user' or 'assistant'")
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class ChatResponse(BaseModel):
    """Chat response data."""
    response: str
    session_id: str
    message_id: str
    model: str
    tokens_used: Optional[int] = None
    latency_ms: Optional[float] = None
    pipeline_stages: Optional[List[str]] = None


class ConversationHistory(BaseModel):
    """Conversation history for a session."""
    session_id: str
    messages: List[Message]
    message_count: int
    created_at: datetime
    last_active: datetime


class SessionCreate(BaseModel):
    """Response when a new session is created."""
    session_id: str
    created_at: datetime
    message: str = "Session created successfully"


# ══════════════════════════════════════════════════════════════════
#  IMAGE ANALYSIS
# ══════════════════════════════════════════════════════════════════

class ImageAnalysisResponse(BaseModel):
    """Image analysis response."""
    analysis: str
    session_id: str
    filename: str
    image_size: Optional[Dict[str, int]] = None
    model: str
    latency_ms: Optional[float] = None


# ══════════════════════════════════════════════════════════════════
#  DOCUMENT ANALYSIS
# ══════════════════════════════════════════════════════════════════

class DocumentAnalysisResponse(BaseModel):
    """Document analysis response."""
    analysis: str
    session_id: str
    filename: str
    file_type: str
    file_size_kb: float
    page_count: Optional[int] = None
    model: str
    latency_ms: Optional[float] = None


# ══════════════════════════════════════════════════════════════════
#  HEALTH
# ══════════════════════════════════════════════════════════════════

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    gemini_status: str
    active_sessions: int
    uptime_seconds: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ModelInfoResponse(BaseModel):
    """Model information response."""
    text_model: str
    vision_model: str
    max_tokens: int
    temperature: float
    rate_limits: Dict[str, str]
    supported_file_types: Dict[str, List[str]]
