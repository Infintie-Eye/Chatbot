"""
Session manager — tracks session lifecycle metadata.
"""
import uuid
import time
import threading
import logging
from typing import Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class Session:
    """Session metadata container."""

    def __init__(self, session_id: str, ttl: int = 3600):
        self.session_id = session_id
        self.created_at = time.time()
        self.last_active = time.time()
        self.message_count = 0
        self.ttl = ttl

    def touch(self):
        self.last_active = time.time()
        self.message_count += 1

    def reset(self):
        self.message_count = 0
        self.touch()

    def is_expired(self) -> bool:
        return (time.time() - self.last_active) > self.ttl

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "created_at": datetime.utcfromtimestamp(self.created_at).isoformat(),
            "last_active": datetime.utcfromtimestamp(self.last_active).isoformat(),
            "message_count": self.message_count,
            "ttl_remaining": max(0, int(self.ttl - (time.time() - self.last_active))),
        }


class SessionManager:
    """Thread-safe session lifecycle manager."""

    def __init__(self):
        self._sessions: Dict[str, Session] = {}
        self._lock = threading.Lock()
        self._ttl = 3600

    def configure(self, ttl: int):
        self._ttl = ttl

    def create_session(self, session_id: Optional[str] = None) -> str:
        session_id = session_id or str(uuid.uuid4())
        with self._lock:
            self._sessions[session_id] = Session(session_id, self._ttl)
        logger.info(f"Session created: {session_id}")
        return session_id

    def get(self, session_id: str) -> Optional[Session]:
        with self._lock:
            return self._sessions.get(session_id)

    def touch(self, session_id: str):
        """Update last_active and increment message count."""
        with self._lock:
            if session_id in self._sessions:
                self._sessions[session_id].touch()
            else:
                # Auto-create if missing
                self._sessions[session_id] = Session(session_id, self._ttl)
                self._sessions[session_id].touch()

    def reset(self, session_id: str):
        with self._lock:
            if session_id in self._sessions:
                self._sessions[session_id].reset()

    def delete(self, session_id: str):
        with self._lock:
            self._sessions.pop(session_id, None)

    def count(self) -> int:
        return len(self._sessions)

    def list_sessions(self) -> list:
        with self._lock:
            return [s.to_dict() for s in self._sessions.values()]

    def evict_expired(self):
        with self._lock:
            expired = [sid for sid, s in self._sessions.items() if s.is_expired()]
            for sid in expired:
                del self._sessions[sid]
            return len(expired)


# Singleton
session_manager = SessionManager()
