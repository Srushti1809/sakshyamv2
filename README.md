# Sakshyam Audio Intelligence Backend

Real audio analysis engine — Whisper AI transcription + criminal keyword detection.

---

## What it does

1. **Receives** your uploaded audio file (WhatsApp voice notes, call recordings, etc.)
2. **Converts** it to optimal WAV format using ffmpeg (handles OPUS, OGG, M4A, everything)
3. **Transcribes** using OpenAI Whisper running locally — no API key, no internet needed
4. **Auto-detects** language (Hindi, English, Marathi, Urdu, Tamil, Bengali — 99 languages)
5. **Tokenizes** the real transcript — removes stopwords, normalises text
6. **Computes** actual word frequency from what was spoken
7. **Scans** 150+ suspicious keywords across 6 crime categories:
   - Financial Crime (hawala, benami, riswat, fraud…)
   - Narcotics (ganja, smack, maal, supari, consignment…)
   - Violence & Threats (maar, khatam, supari, gun, bomb…)
   - Cyber Crime (hack, phishing, OTP, clone, darkweb…)
   - Terrorism (IED, fidayeen, sleeper, handler…)
   - Conspiracy & Evasion (bhaag, nikal, saboot, chhupa…)
8. **Maps each keyword** to exact timestamp in audio
9. **Scores threat** 0–100 based on keyword severity and frequency
10. **Returns** structured JSON that the frontend renders directly

---

## Setup (5 minutes)

### Prerequisites

**Python 3.9+**
```bash
python --version  # must be 3.9 or higher
```

**ffmpeg** (required to decode OPUS/OGG/M4A/AMR)
```bash
# Mac
brew install ffmpeg

# Ubuntu / Debian
sudo apt update && sudo apt install ffmpeg -y

# Windows
# Download from https://ffmpeg.org/download.html
# Extract, add the /bin folder to your PATH environment variable
# Then restart your terminal

# Verify
ffmpeg -version
```

---

### Install Python packages

```bash
cd sakshyam-audio-backend
pip install -r requirements.txt
```

> **First run** downloads the Whisper `base` model (~145 MB, one-time only).

---

### Start the server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

Open http://localhost:8000/docs to test the API interactively.

---

### Open the frontend

Open `Sakshyam-v2.html` in your browser. The site auto-detects the backend:

| Badge | Meaning |
|-------|---------|
| `⚡ AI BACKEND ONLINE` | Real Whisper transcription active |
| `⚠ SIMULATION MODE` | Backend offline — mock data shown |

---

## API Reference

### `GET /api/health`
Check server status.
```json
{
  "status": "online",
  "whisper": "available",
  "ffmpeg": "available"
}
```

### `POST /api/audio/analyse`
Upload audio file, get full analysis.

**Request:** `multipart/form-data` with field `file`

**Accepted formats:** MP3, WAV, OGG, OPUS, M4A, FLAC, AAC, WMA, WEBM, 3GP, AMR

**Response:**
```json
{
  "status": "success",
  "file": {
    "name": "recording.opus",
    "size_mb": 0.42,
    "format": "OPUS"
  },
  "transcription": {
    "text": "Full transcript text here...",
    "language": "hi",
    "language_display": "Hindi",
    "segments_count": 18,
    "word_count": 312,
    "transcription_time_sec": 14.2
  },
  "metrics": {
    "duration_sec": 87.4,
    "duration_display": "1m 27s",
    "speech_ratio": 82,
    "speaking_rate_wpm": 145,
    "segment_count": 18
  },
  "speakers": ["Speaker 1", "Speaker 2"],
  "transcript_lines": [
    {"t": "00:00", "spk": 0, "txt": "Bhai transfer ho gaya kya?", "start": 0.0, "end": 3.2}
  ],
  "analysis": {
    "score": 74,
    "score_color": "#f59e0b",
    "score_label": "🟡 HIGH RISK — Suspicious communication detected.",
    "susp_total": 8,
    "susp_found": [
      {
        "word": "transfer",
        "count": 3,
        "level": "high",
        "meaning": "Money transfer — possible hawala",
        "ipc": "PMLA §3",
        "category": "Financial Crime",
        "color": "#f97316",
        "timestamps": ["00:00", "00:22", "01:14"]
      }
    ],
    "by_category": {
      "Financial Crime": 5,
      "Conspiracy / Evasion": 3
    },
    "top20_words": [
      {"word": "transfer", "count": 3},
      {"word": "paisa", "count": 2}
    ],
    "word_freq": {"transfer": 3, "paisa": 2, "bhai": 4}
  }
}
```

---

## Whisper Model Selection

Edit `api/engine.py` line: `_whisper_model_name = "base"`

| Model | Download Size | RAM Usage | Speed (1 min audio) | Accuracy |
|-------|--------------|-----------|---------------------|----------|
| `tiny`   | 39 MB  | 1 GB  | ~5s   | Good         |
| `base`   | 74 MB  | 1 GB  | ~15s  | **Default ✅** |
| `small`  | 244 MB | 2 GB  | ~45s  | Better Hindi/Marathi |
| `medium` | 769 MB | 5 GB  | ~2min | Excellent    |
| `large`  | 1.5 GB | 10 GB | ~5min | Best         |

**Recommendation:** Use `small` for best Hindi/Marathi accuracy if your machine has 4GB+ RAM.

---

## Troubleshooting

**`No module named 'whisper'`**
```bash
pip install openai-whisper
```

**`ffmpeg: command not found`**
Install ffmpeg (see Prerequisites above). Whisper needs it for audio decoding.

**OPUS / WhatsApp files not working**
Make sure ffmpeg is installed. OPUS files require ffmpeg for decoding.

**Slow transcription**
Use `tiny` model for speed, or `small` for balance. The first call is slow (model loading), subsequent calls are fast.

**CORS error in browser**
Make sure the server is running on port 8000. The frontend calls `http://localhost:8000`.

**`413 File too large`**
Max file size is 100MB. Compress or trim the audio first.
