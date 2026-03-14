"""
Sakshyam Audio Analysis Engine
================================
- Transcribes audio using OpenAI Whisper (local, no API key)
- Detects language automatically
- Computes word frequency from REAL transcript
- Flags suspicious keywords with IPC sections
- Scores threat level
- Returns structured JSON matching frontend expectations exactly
"""

import os
import re
import time
import math
import tempfile
import subprocess
from collections import Counter
from typing import Optional

from api.keywords import KEYWORDS, LEVEL_COLORS, STOPWORDS, CATEGORY_LABELS


# ─── WHISPER LOADER (singleton — load model once) ─────────────────────────────
_whisper_model = None
_whisper_model_name = "base"

def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        try:
            import whisper
            print(f"[Whisper] Loading '{_whisper_model_name}' model…")
            _whisper_model = whisper.load_model(_whisper_model_name)
            print("[Whisper] Model ready.")
        except ImportError:
            raise RuntimeError("openai-whisper not installed. Run: pip install openai-whisper")
    return _whisper_model


# ─── AUDIO CONVERSION ─────────────────────────────────────────────────────────
def convert_to_wav(input_path: str, output_dir: str) -> str:
    """
    Convert any audio format → 16kHz mono WAV (optimal for Whisper).
    Uses ffmpeg. Supports: MP3, OGG, OPUS, M4A, FLAC, AAC, AMR, 3GP, WEBM, WMA.
    """
    wav_path = os.path.join(output_dir, "audio_converted.wav")
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-ar", "16000",       # 16kHz sample rate
        "-ac", "1",            # mono
        "-acodec", "pcm_s16le", # 16-bit PCM
        wav_path,
        "-loglevel", "error"
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0 or not os.path.exists(wav_path):
        # Fallback: try direct path
        return input_path
    return wav_path


def get_audio_duration(wav_path: str) -> float:
    """Get audio duration in seconds using ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", wav_path],
            capture_output=True, text=True
        )
        return float(result.stdout.strip())
    except Exception:
        return 0.0


# ─── TRANSCRIPTION ────────────────────────────────────────────────────────────
def transcribe(wav_path: str) -> dict:
    """
    Run Whisper transcription.
    Returns: {text, language, language_display, segments, duration_sec}
    """
    model = get_whisper_model()

    t_start = time.time()
    result = model.transcribe(
        wav_path,
        language=None,           # auto-detect
        task="transcribe",
        verbose=False,
        fp16=False,              # safer on CPU
        word_timestamps=True,    # get word-level timing
        condition_on_previous_text=True,
        no_speech_threshold=0.5,
        compression_ratio_threshold=2.4,
    )
    elapsed = round(time.time() - t_start, 2)

    lang = result.get("language", "unknown")
    segments = result.get("segments", [])

    return {
        "text": result["text"].strip(),
        "language": lang,
        "language_display": LANGUAGE_MAP.get(lang, lang.upper()),
        "segments": [
            {
                "start": round(s["start"], 2),
                "end":   round(s["end"],   2),
                "text":  s["text"].strip(),
                "words": [
                    {"word": w["word"].strip(), "start": round(w["start"],2), "end": round(w["end"],2)}
                    for w in s.get("words", [])
                ] if s.get("words") else [],
            }
            for s in segments
        ],
        "duration_sec": get_audio_duration(wav_path) or (segments[-1]["end"] if segments else 0),
        "transcription_time": elapsed,
    }


# ─── SPEAKER DIARIZATION (simple heuristic) ──────────────────────────────────
def assign_speakers(segments: list) -> list:
    """
    Simple speaker diarization based on silence gaps.
    Gap > 1.5s = likely new speaker.
    Returns segments with .spk assigned (0 or 1).
    """
    result = []
    current_speaker = 0
    last_end = 0.0
    for seg in segments:
        gap = seg["start"] - last_end
        if gap > 1.5 and last_end > 0:
            current_speaker = 1 - current_speaker
        result.append({**seg, "spk": current_speaker})
        last_end = seg["end"]
    return result


# ─── WORD ANALYSIS ────────────────────────────────────────────────────────────
def tokenize(text: str) -> list[str]:
    """
    Clean and tokenize transcript text.
    Handles English, Hindi (roman), Marathi.
    """
    # Lowercase
    text = text.lower()
    # Keep letters, digits, spaces, Devanagari
    text = re.sub(r"[^\w\u0900-\u097f\s]", " ", text)
    words = text.split()
    # Filter: min 2 chars, not a stopword, not pure digits
    return [w for w in words if len(w) >= 2 and w not in STOPWORDS and not w.isdigit()]


def compute_word_frequency(words: list[str]) -> dict:
    """Full word frequency map sorted by count descending."""
    return dict(Counter(words).most_common())


def get_top_words(freq: dict, n: int = 20) -> list[dict]:
    """Top N words as [{word, count}]."""
    return [{"word": w, "count": c} for w, c in list(freq.items())[:n]]


# ─── KEYWORD DETECTION ────────────────────────────────────────────────────────
def detect_keywords(words: list[str], segments: list) -> dict:
    """
    Scan for suspicious keywords in word list.
    Also maps each keyword to timestamps from segments.

    Returns:
        susp_found: list of rich keyword objects
        susp_total: total count of suspicious word occurrences
        by_category: grouped counts
        score: 0–100 threat score
    """
    # Build word → [timestamps] map from segments
    word_timestamps: dict[str, list[str]] = {}
    for seg in segments:
        for word_entry in seg.get("words", []):
            w = word_entry["word"].lower().strip()
            w_clean = re.sub(r"[^\w]", "", w)
            if w_clean not in word_timestamps:
                word_timestamps[w_clean] = []
            ts = _sec_to_ts(word_entry["start"])
            if ts not in word_timestamps[w_clean]:
                word_timestamps[w_clean].append(ts)
        # Also scan segment text for keywords without word timestamps
        seg_words = tokenize(seg["text"])
        for sw in seg_words:
            if sw in KEYWORDS and sw not in word_timestamps:
                word_timestamps[sw] = [_sec_to_ts(seg["start"])]
            elif sw in KEYWORDS:
                ts = _sec_to_ts(seg["start"])
                if ts not in word_timestamps[sw]:
                    word_timestamps[sw].append(ts)

    # Count each keyword in full word list
    word_counter = Counter(words)
    susp_found = []
    susp_total = 0
    by_category: dict[str, int] = {}

    for word, count in word_counter.most_common():
        if word in KEYWORDS:
            meta = KEYWORDS[word]
            susp_total += count
            cat = meta["category"]
            by_category[cat] = by_category.get(cat, 0) + count
            susp_found.append({
                "word":       word,
                "count":      count,
                "level":      meta["level"],
                "meaning":    meta["meaning"],
                "ipc":        meta["ipc"],
                "category":   CATEGORY_LABELS.get(cat, cat),
                "color":      LEVEL_COLORS[meta["level"]],
                "timestamps": word_timestamps.get(word, [])[:6],
            })

    # Sort by severity then count
    level_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    susp_found.sort(key=lambda x: (level_order[x["level"]], -x["count"]))

    # Threat score
    crit  = sum(x["count"] for x in susp_found if x["level"] == "critical")
    high  = sum(x["count"] for x in susp_found if x["level"] == "high")
    med   = sum(x["count"] for x in susp_found if x["level"] == "medium")
    score = min(100, int(crit * 20 + high * 10 + med * 4 + min(susp_total * 2, 20)))

    return {
        "susp_found":   susp_found,
        "susp_total":   susp_total,
        "by_category":  {CATEGORY_LABELS.get(k,k): v for k,v in by_category.items()},
        "score":        score,
        "score_color":  LEVEL_COLORS["critical"] if score > 75 else LEVEL_COLORS["high"] if score > 50 else "#22c55e",
        "score_label":  (
            "🔴 CRITICAL — Immediate action required. File FIR and request CDR." if score > 75
            else "🟡 HIGH RISK — Suspicious communication detected. Flag for monitoring." if score > 50
            else "🟢 LOW RISK — No major threats found. Log and archive."
        ),
    }


# ─── TRANSCRIPT LINES (frontend format) ──────────────────────────────────────
def build_transcript_lines(segments_with_speakers: list) -> list:
    """
    Convert segments → [{t, spk, txt}] for the frontend transcript renderer.
    """
    lines = []
    for seg in segments_with_speakers:
        if not seg["text"].strip():
            continue
        lines.append({
            "t":     _sec_to_ts(seg["start"]),
            "spk":   seg["spk"],
            "txt":   seg["text"].strip(),
            "start": seg["start"],
            "end":   seg["end"],
        })
    return lines


# ─── AUDIO METRICS ────────────────────────────────────────────────────────────
def compute_audio_metrics(segments: list, duration_sec: float) -> dict:
    """Compute speaking rate, silence ratio, etc."""
    if not segments or duration_sec <= 0:
        return {}
    total_speech = sum(s["end"] - s["start"] for s in segments)
    silence = max(0, duration_sec - total_speech)
    all_text = " ".join(s["text"] for s in segments)
    word_count = len(all_text.split())
    speaking_rate = round(word_count / (total_speech / 60)) if total_speech > 0 else 0

    return {
        "duration_sec":     round(duration_sec, 1),
        "duration_display": _sec_to_display(duration_sec),
        "speech_ratio":     round(total_speech / duration_sec * 100),
        "silence_sec":      round(silence, 1),
        "speaking_rate_wpm": speaking_rate,
        "segment_count":    len(segments),
    }


# ─── FULL ANALYSIS PIPELINE ───────────────────────────────────────────────────
def analyse_audio_file(file_path: str, filename: str, file_size: int) -> dict:
    """
    Full pipeline: convert → transcribe → analyse → return structured result.
    This is called by the API route.
    """
    tmp_dir = tempfile.mkdtemp()
    try:
        # Step 1: Convert to WAV
        wav_path = convert_to_wav(file_path, tmp_dir)

        # Step 2: Transcribe
        transcription = transcribe(wav_path)
        segments = assign_speakers(transcription["segments"])

        # Step 3: Tokenize
        full_text = transcription["text"]
        words = tokenize(full_text)

        # Step 4: Word frequency
        freq = compute_word_frequency(words)
        top20 = get_top_words(freq, 20)

        # Step 5: Keyword detection
        kw_analysis = detect_keywords(words, segments)

        # Step 6: Transcript lines
        transcript_lines = build_transcript_lines(segments)

        # Step 7: Audio metrics
        metrics = compute_audio_metrics(
            transcription["segments"],
            transcription["duration_sec"]
        )

        # Step 8: Speaker count
        speakers_detected = len(set(s["spk"] for s in segments)) if segments else 1
        speaker_labels = [f"Speaker {i+1}" for i in range(speakers_detected)]

        return {
            "status": "success",
            "file": {
                "name":     filename,
                "size_mb":  round(file_size / 1048576, 2),
                "size_display": _format_size(file_size),
                "format":   filename.rsplit(".", 1)[-1].upper() if "." in filename else "UNKNOWN",
            },
            "transcription": {
                "text":               full_text,
                "language":           transcription["language"],
                "language_display":   transcription["language_display"],
                "segments_count":     len(segments),
                "word_count":         len(words),
                "transcription_time_sec": transcription["transcription_time"],
            },
            "metrics":   metrics,
            "speakers":  speaker_labels,
            "transcript_lines": transcript_lines,
            "analysis": {
                "score":        kw_analysis["score"],
                "score_color":  kw_analysis["score_color"],
                "score_label":  kw_analysis["score_label"],
                "susp_total":   kw_analysis["susp_total"],
                "susp_found":   kw_analysis["susp_found"],
                "by_category":  kw_analysis["by_category"],
                "top20_words":  top20,
                "word_freq":    dict(list(freq.items())[:30]),
            },
        }

    finally:
        import shutil
        shutil.rmtree(tmp_dir, ignore_errors=True)


# ─── HELPERS ──────────────────────────────────────────────────────────────────
def _sec_to_ts(sec: float) -> str:
    sec = int(sec)
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def _sec_to_display(sec: float) -> str:
    sec = int(sec)
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m}m {s}s"
    if m:
        return f"{m}m {s}s"
    return f"{s}s"


def _format_size(b: int) -> str:
    if b >= 1048576:
        return f"{b/1048576:.1f} MB"
    return f"{b/1024:.0f} KB"


LANGUAGE_MAP = {
    "hi": "Hindi", "en": "English", "mr": "Marathi", "ur": "Urdu",
    "ta": "Tamil", "te": "Telugu", "bn": "Bengali", "gu": "Gujarati",
    "pa": "Punjabi", "kn": "Kannada", "ml": "Malayalam", "or": "Odia",
    "as": "Assamese", "ne": "Nepali", "si": "Sinhala",
    "zh": "Chinese", "ar": "Arabic", "fa": "Persian/Farsi",
    "unknown": "Auto-detected",
}
