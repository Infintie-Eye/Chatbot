# Changelog

All notable changes to Conrux AI are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [3.0.0] — 2026-02-27

### ✦ Major Release — Production Expert Chatbot

This release is a full architectural overhaul, replacing the Streamlit prototype with a production-ready FastAPI stack.

### Added
- **FastAPI backend** (`api/`) serving REST API at `/api/v1/`
- **4-stage data pipeline** (`src/pipeline/`): input → context → ai → output
- **Pydantic v2 schemas** for all request/response models
- **Session management** — thread-safe sessions with TTL auto-expiry
- **In-memory conversation history** — thread-safe with rolling window + TTL eviction
- **Rate limiting** using `slowapi` (30 chat RPM, 10 analysis RPM)
- **Optional API key authentication** via `X-API-Key` header
- **Request logging middleware** — unique request IDs, latency headers
- **Image analysis endpoint** — multipart upload with PIL processing
- **Document analysis endpoint** — PDF, DOCX, TXT, CSV, JSON, XLSX support
- **Luxury frontend** (`frontend/`) — art-deco black-gold design
  - Geometric canvas background (hexagons, diamonds, fan corners)
  - Floating gold particle animation
  - Custom inline SVG icons
  - Multi-section layout: Chat, Vision, Documents
  - Drag-and-drop file upload zones
  - Toast notifications and scroll-spy navbar
- **Postman collection** with 8 endpoints and automated test assertions
- **`run_api.py`** quick-start launcher
- `CONTRIBUTING.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`
- GitHub issue templates and pull request template

### Changed
- Model switched to `models/gemini-2.5-flash-lite` (free-tier compatible)
- `config/settings.py` — full rewrite with Pydantic-settings, all env vars documented
- `requirements.txt` — updated with FastAPI, uvicorn, slowapi, structlog, etc.
- `README.md` — complete rewrite with accurate structure, API reference, pipeline diagram
- `.gitignore` — updated to exclude venv, logs, `.env`, `__pycache__`

### Removed
- Legacy `app.py` (deprecated Streamlit redirect stub)
- `setup.py`, `pyproject.toml` (unused packaging)
- `SETUP_GUIDE.md` (superseded by new README)
- `static/` directory (replaced by `frontend/`)
- `__pycache__` directories
- `.streamlit/` configuration

---

## [2.0.0] — 2025-12-01

### Added
- Upgraded from Gemini 1.5 to Gemini 2.0 Flash
- Enhanced image analysis with improved accuracy
- Larger context window (8192 tokens)
- Streamlit multi-tab layout (Chat, Image Analysis, Document Processing)
- `src/core/gemini_client.py` — dedicated API client with retry logic

### Changed
- Increased max file upload size to 20 MB
- Improved error handling and user feedback

---

## [1.0.0] — 2025-11-20

### Added
- Initial Streamlit chatbot prototype
- Basic text chat with Gemini API
- Image upload and analysis
- Document processing (TXT, PDF)
- Session-based chat history
