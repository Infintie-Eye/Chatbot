"""
In-memory conversation memory manager with TTL eviction.
Stores conversation history as Gemini-compatible message dicts.
"""
import time
import logging
import threading
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class ConversationMessage:
    """A single conversation message."""

    __slots__ = ("role", "content", "timestamp", "message_id")

    def __init__(self, role: str, content: str, message_id: str = None):
        import uuid
        self.role = role
        self.content = content
        self.timestamp = datetime.utcnow()
        self.message_id = message_id or str(uuid.uuid4())

    def model_dump(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "message_id": self.message_id,
        }

    def to_gemini_format(self) -> Dict[str, Any]:
        """Convert to Gemini's expected history format."""
        # Gemini uses 'model' for assistant, 'user' for user
        gemini_role = "model" if self.role == "assistant" else "user"
        return {"role": gemini_role, "parts": [self.content]}


class SessionBuffer:
    """Conversation buffer for a single session."""

    def __init__(self, session_id: str, ttl: int = 3600, max_messages: int = 50):
        self.session_id = session_id
        self.ttl = ttl
        self.max_messages = max_messages
        self.messages: List[ConversationMessage] = []
        self.created_at = time.time()
        self._last_access = time.time()

    def add_message(self, role: str, content: str) -> ConversationMessage:
        msg = ConversationMessage(role, content)
        self.messages.append(msg)
        self._last_access = time.time()
        # Rolling window — keep last max_messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
        return msg

    def get_history(self) -> List[ConversationMessage]:
        self._last_access = time.time()
        return self.messages

    def get_gemini_history(self, last_n: Optional[int] = None) -> List[Dict]:
        """Return history in Gemini chat format."""
        msgs = self.messages[-last_n:] if last_n else self.messages
        return [m.to_gemini_format() for m in msgs]

    def clear(self):
        self.messages = []

    def is_expired(self) -> bool:
        return (time.time() - self._last_access) > self.ttl


class MemoryManager:
    """Thread-safe manager for all conversation session buffers."""

    def __init__(self):
        self._sessions: Dict[str, SessionBuffer] = {}
        self._lock = threading.Lock()
        self._ttl = 3600
        self._max_messages = 50

    def configure(self, ttl: int, max_messages: int):
        self._ttl = ttl
        self._max_messages = max_messages

    def _get_or_create(self, session_id: str) -> SessionBuffer:
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionBuffer(
                session_id, self._ttl, self._max_messages
            )
        return self._sessions[session_id]

    def add_message(self, session_id: str, role: str, content: str) -> ConversationMessage:
        """Add a message to a session's memory."""
        with self._lock:
            self._evict_expired()
            buf = self._get_or_create(session_id)
            return buf.add_message(role, content)

    def get_history(self, session_id: str) -> Optional[List[ConversationMessage]]:
        """Get conversation history. Returns None if session not found."""
        with self._lock:
            buf = self._sessions.get(session_id)
            if buf is None:
                return None
            return buf.get_history()

    def get_gemini_history(self, session_id: str, last_n: Optional[int] = None) -> List[Dict]:
        """Get history in Gemini API format."""
        with self._lock:
            buf = self._sessions.get(session_id)
            if buf is None:
                return []
            return buf.get_gemini_history(last_n)

    def clear(self, session_id: str):
        """Clear a session's messages."""
        with self._lock:
            if session_id in self._sessions:
                self._sessions[session_id].clear()

    def delete_session(self, session_id: str):
        """Fully remove a session."""
        with self._lock:
            self._sessions.pop(session_id, None)

    def count(self) -> int:
        return len(self._sessions)

    def _evict_expired(self):
        """Remove expired sessions (call with lock held)."""
        expired = [sid for sid, buf in self._sessions.items() if buf.is_expired()]
        for sid in expired:
            logger.debug(f"Evicting expired session: {sid}")
            del self._sessions[sid]


# Singleton
memory_manager = MemoryManager()
