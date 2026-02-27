# ✦ Conrux AI — Elite Intelligence

<div align="center">

**A production-ready Expert AI Chatbot by [Blacifer](https://www.blacifer.com)**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.133%2B-009688?style=flat-square&logo=fastapi)
![Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-4285F4?style=flat-square&logo=google)
![License](https://img.shields.io/badge/License-MIT-gold?style=flat-square)

*Conversation meets artistry — a luxury AI chatbot with a production backend, 4-stage data pipeline, and an art-deco black-gold frontend.*

</div>

---

## 🖼️ Preview

> **Frontend** → art-deco black & gold theme • geometric canvas animations • custom SVG icons  
> **Backend** → FastAPI REST API • 4-stage pipeline • multi-turn memory • rate limiting

---

## ✦ Features

| Capability | Details |
|---|---|
| 💬 **Multi-turn Chat** | Session-based conversation memory with TTL eviction |
| 🔭 **4-Stage Pipeline** | Input → Context → AI → Output with per-stage timing |
| 🖼️ **Vision Analysis** | Upload images (JPG, PNG, WEBP, GIF) for AI visual insight |
| 📄 **Document Processing** | PDF, DOCX, TXT, CSV, JSON, XLSX — up to 20 MB |
| 🔐 **Optional Auth** | `X-API-Key` header auth, disable with no env var |
| ⚡ **Rate Limiting** | Configurable per-minute caps via `slowapi` |
| 🗂️ **Session Management** | Thread-safe sessions with auto-expiry |
| 📋 **Postman Collection** | Full API collection with automated tests |
| 🌐 **Luxury Frontend** | Black-gold art-deco HTML/CSS/JS served directly from FastAPI |

---

## 🏗️ Project Structure

```
Conrux-AI/
├── api/                        # FastAPI application layer
│   ├── main.py                 # App factory — mounts frontend & routers
│   ├── routers/
│   │   ├── chat.py             # POST /chat, GET/DELETE /chat/history/{id}
│   │   ├── health.py           # GET /health, /info
│   │   ├── images.py           # POST /analyze/image
│   │   └── documents.py        # POST /analyze/document
│   ├── models/
│   │   └── schemas.py          # Pydantic v2 request/response schemas
│   └── middleware/
│       ├── auth.py             # Optional X-API-Key authentication
│       └── logging_middleware.py  # Request ID + latency headers
│
├── src/
│   ├── core/
│   │   ├── gemini_client.py    # Gemini API client (legacy SDK, free-tier compatible)
│   │   ├── memory_manager.py   # Thread-safe in-memory conversation store + TTL
│   │   └── session_manager.py  # Session lifecycle management
│   ├── pipeline/
│   │   ├── pipeline_manager.py # Orchestrates all 4 stages
│   │   └── stages/
│   │       ├── input_stage.py  # Validation, sanitisation, injection detection
│   │       ├── context_stage.py # Load history, apply system prompt
│   │       ├── ai_stage.py     # Call Gemini, measure latency
│   │       └── output_stage.py # Persist to memory, build result payload
│   ├── ui/                     # Legacy Streamlit components (kept for reference)
│   └── utils/
│       └── file_processor.py   # File reading, type detection
│
├── config/
│   └── settings.py             # Pydantic-settings — all config from .env
│
├── frontend/                   # Luxury static frontend (served by FastAPI at /)
│   ├── index.html              # Art-deco HTML with inline SVG icons
│   ├── css/main.css            # Black-gold design system
│   └── js/app.js               # Dynamic chat, upload, geometric canvas
│
├── postman/
│   └── Chatbot_API_Collection.json   # Full Postman collection
│
├── assets/                     # Static assets (logo etc.)
├── main.py                     # Legacy Streamlit entry (unused — see run_api.py)
├── run_api.py                  # ✅ Quick-start launcher
├── requirements.txt
├── .env.example                # All env variables documented
└── .gitignore
```

---

## 🚀 Quick Start

### 1. Prerequisites

- Python **3.10+**
- A **Google Gemini API key** → [Get one at Google AI Studio](https://aistudio.google.com/)

### 2. Clone & Install

```bash
git clone https://github.com/your-username/conrux-ai.git
cd conrux-ai

python -m venv venv
# Windows:  venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Open .env and set your key:
# GEMINI_API_KEY=your_key_here
```

### 4. Run

```bash
python run_api.py
```

| URL | Description |
|---|---|
| `http://localhost:8000` | 🌐 Luxury frontend |
| `http://localhost:8000/docs` | 📋 Swagger API docs |
| `http://localhost:8000/redoc` | 📖 ReDoc API docs |

---

## 🔧 Configuration Reference

All settings are loaded from `.env` (see `.env.example` for full reference):

| Variable | Default | Description |
|---|---|---|
| `GEMINI_API_KEY` | — | **Required.** Your Google Gemini API key |
| `CHATBOT_API_KEY` | — | Optional. Enables `X-API-Key` auth on all routes |
| `TEXT_MODEL` | `models/gemini-2.5-flash-lite` | Gemini model for text |
| `VISION_MODEL` | `models/gemini-2.5-flash-lite` | Gemini model for vision |
| `MAX_TOKENS` | `2048` | Max output tokens per response |
| `TEMPERATURE` | `0.7` | Model creativity (0.0–1.0) |
| `API_PORT` | `8000` | FastAPI server port |
| `SESSION_TTL_SECONDS` | `3600` | Session expiry (1 hour) |
| `MAX_CONTEXT_MESSAGES`| `20` | Message pairs kept in context |
| `MAX_FILE_SIZE_MB` | `20` | Upload limit |
| `RATE_LIMIT_CHAT` | `30/minute` | Chat endpoint rate limit |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

> **Tip:** Check which models your API key supports by running:
> ```bash
> python -c "import google.generativeai as g, os; g.configure(api_key=os.getenv('GEMINI_API_KEY')); [print(m.name) for m in g.list_models() if 'generateContent' in m.supported_generation_methods]"
> ```

---

## 📡 API Reference

Base URL: `http://localhost:8000/api/v1`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check + Gemini connectivity |
| `GET` | `/info` | Model config & feature flags |
| `POST` | `/chat/session` | Create a new session |
| `POST` | `/chat` | Send a message (multi-turn) |
| `GET` | `/chat/history/{session_id}` | Get conversation history |
| `DELETE`| `/chat/history/{session_id}` | Clear history |
| `POST` | `/analyze/image` | Analyse an uploaded image |
| `POST` | `/analyze/document` | Analyse an uploaded document |

📦 **Postman:** Import `postman/Chatbot_API_Collection.json` — includes automated test assertions for every endpoint.

---

## 🔄 Data Pipeline

Every chat message flows through 4 sequential stages:

```
User Input
    │
    ▼
┌─────────────────────────────────────┐
│ 1. INPUT STAGE                      │
│  Validate length · Sanitise ·       │
│  Detect prompt injection · Add ID   │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│ 2. CONTEXT STAGE                    │
│  Load session history · Apply       │
│  system prompt · Trim context       │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│ 3. AI STAGE                         │
│  Call Gemini · Multi-turn or        │
│  single turn · Measure latency      │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│ 4. OUTPUT STAGE                     │
│  Persist to memory · Build result   │
│  payload · Update session           │
└────────────────┬────────────────────┘
                 │
                 ▼
         Structured JSON Response
```

---

## 🐛 Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `404 NOT_FOUND: models/...` | Model not available on your API key | Run the model lister above; use a model from the output |
| `429 RESOURCE_EXHAUSTED` | Per-minute rate limit hit | Wait 60 seconds and retry |
| `No module named 'pydantic_settings'` | Missing dependency | `pip install pydantic-settings` |
| Frontend shows `{"detail":"Not Found"}` | Wrong working directory | Run from the `Chatbot/` root: `python run_api.py` |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make changes and add tests where applicable
4. Open a pull request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Made with ✦ by Blacifer**  
Powered by Google Gemini · Built with FastAPI

</div>