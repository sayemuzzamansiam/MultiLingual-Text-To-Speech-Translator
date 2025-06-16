# app/api/endpoints/translator.py

from fastapi import APIRouter
from app.services.translation_service import translate_text
from app.services.tts_service import generate_speech
from app.api.models.translator_models import TranslationRequest, TranslationResponse

router = APIRouter()

@router.post("/translate", response_model=TranslationResponse)
def handle_translation(request: TranslationRequest):
    """
    Translates the input text, then converts the translated text into speech.
    """
    # Step 1: Translate text
    translated_text = translate_text(
        source_language=request.source_language,
        target_language=request.target_language,
        text=request.text
    )

    # Step 2: Convert to speech using translated text
    audio_path = generate_speech(translated_text, voice=request.voice)

    return TranslationResponse(
        translated_text=translated_text,
        audio_file_path=audio_path
    )
