"""
Conrux AI Expert Chatbot — Quick Launch Script
Run this file directly OR use:
    uvicorn api.main:app --reload --port 8000
"""
import subprocess
import sys
import os
from pathlib import Path

ROOT = Path(__file__).parent
os.chdir(ROOT)  # ensure cwd is the project root

# Add project root to PYTHONPATH
sys.path.insert(0, str(ROOT))

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════╗
║         CONRUX AI — Expert Chatbot v3.0.0            ║
║         Powered by Google Gemini 2.0 Flash           ║
╠══════════════════════════════════════════════════════╣
║  Frontend  →  http://localhost:8000                  ║
║  API Docs  →  http://localhost:8000/docs             ║
║  ReDoc     →  http://localhost:8000/redoc            ║
╚══════════════════════════════════════════════════════╝
    """)

    try:
        import uvicorn
        uvicorn.run(
            "api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
        )
    except ImportError:
        print("uvicorn not found. Install requirements first:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
