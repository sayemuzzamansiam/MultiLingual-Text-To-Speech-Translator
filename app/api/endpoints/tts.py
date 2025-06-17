# app/api/endpoints/tts.py

from fastapi import APIRouter
from app.api.models.tts_models import TTSRequest, TTSResponse
from app.services.tts_service import generate_speech

router = APIRouter()

@router.post("/tts", response_model=TTSResponse)
def handle_tts(request: TTSRequest):
    """
    Generate speech from text using Gemini TTS and return the audio file path.
    """
    audio_path = generate_speech(request.text, voice=request.voice)
    return TTSResponse(audio_file_path=audio_path)
