"""
Audio Analysis API Route
Accepts: MP3, WAV, OGG, OPUS, M4A, FLAC, AAC, WMA, WEBM, 3GP, AMR
Returns: Full structured JSON matching Sakshyam frontend exactly
"""

import os
import tempfile
import traceback

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from api.engine import analyse_audio_file

router = APIRouter()

# Max file size: 100 MB
MAX_FILE_SIZE = 100 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".mp3", ".wav", ".ogg", ".opus", ".m4a", ".flac",
    ".aac", ".wma", ".webm", ".3gp", ".amr", ".mpeg", ".mp4"
}


@router.post("/analyse")
async def analyse_audio(file: UploadFile = File(...)):
    """
    Upload any audio file → real Whisper transcription + full threat analysis.

    Response shape (matches Sakshyam frontend mapAudioBackendResponse):
    {
      status, file, transcription, metrics, speakers,
      transcript_lines, analysis: { score, score_color, score_label,
        susp_total, susp_found, by_category, top20_words, word_freq }
    }
    """
    filename = file.filename or "upload"
    ext = os.path.splitext(filename)[1].lower()

    if ext and ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format '{ext}'. Supported: MP3, WAV, OGG, OPUS, M4A, FLAC, AAC, WMA, WEBM, 3GP, AMR"
        )

    tmp_dir = tempfile.mkdtemp()
    file_path = os.path.join(tmp_dir, filename)

    try:
        # Read and save
        content = await file.read()
        file_size = len(content)

        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail=f"File too large ({file_size//1048576}MB). Max 100MB.")

        if file_size < 100:
            raise HTTPException(status_code=400, detail="File appears empty or too small.")

        with open(file_path, "wb") as f:
            f.write(content)

        # Run full analysis pipeline
        result = analyse_audio_file(file_path, filename, file_size)
        return JSONResponse(result)

    except HTTPException:
        raise

    except RuntimeError as e:
        # Whisper not installed etc.
        raise HTTPException(status_code=503, detail=str(e))

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    finally:
        import shutil
        shutil.rmtree(tmp_dir, ignore_errors=True)
