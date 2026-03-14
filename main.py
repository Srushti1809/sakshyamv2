"""
Sakshyam Audio Intelligence Backend
====================================
Real audio analysis engine for the Sakshyam police investigation dashboard.

Start: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
Docs:  http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.audio import router as audio_router

app = FastAPI(
    title="Sakshyam Audio Intelligence API",
    description="Real-time audio transcription, keyword detection, and threat analysis",
    version="1.0.0",
)

# Allow browser (file:// or localhost) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(audio_router, prefix="/api/audio")


@app.get("/api/health")
def health():
    return {
        "status": "online",
        "service": "Sakshyam Audio Intelligence",
        "version": "1.0.0",
        "whisper": _check_whisper(),
        "ffmpeg": _check_ffmpeg(),
    }


def _check_whisper() -> str:
    try:
        import whisper
        return "available"
    except ImportError:
        return "not installed — run: pip install openai-whisper"


def _check_ffmpeg() -> str:
    import subprocess
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return "available"
    except Exception:
        return "not found — install ffmpeg"
