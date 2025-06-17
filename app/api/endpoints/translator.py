# app/api/endpoints/translator.py

import os
import time  # Import the time module
from fastapi import APIRouter, HTTPException, Request

# Import our two core services
from app.services.translation_service import translate_text
from app.services.tts_service import generate_speech

# Import our Pydantic models
from app.api.models.translator_models import TranslationRequest, FullTranslationResponse

router = APIRouter()

# Note: The code provided includes a duplicate router. We will only use one.
@router.post("/translate", response_model=FullTranslationResponse, tags=["Translation"])
async def handle_full_translation_flow(req_body: TranslationRequest, request: Request):
    """
    Translates text, generates speech, and returns a JSON response containing
    the translated text, a public URL to the audio file, and performance metrics.
    """
    # === START TIMING ===
    start_time = time.perf_counter()

    # Step 1: Translate
    translated_text = translate_text(
        source_language=req_body.source_language,
        target_language=req_body.target_language,
        text=req_body.text
    )
    translation_end_time = time.perf_counter()

    if "Error:" in translated_text:
        raise HTTPException(status_code=500, detail=f"Translation Error: {translated_text}")

    # Step 2: Generate Speech
    audio_file_path = generate_speech(text=translated_text, voice=req_body.voice)
    tts_end_time = time.perf_counter()
    
    if "Error:" in audio_file_path:
        raise HTTPException(status_code=500, detail=f"Speech Generation Error: {audio_file_path}")

    # Step 3: Construct the Public URL
    base_url = str(request.base_url)
    public_audio_url = f"{base_url}audio/{os.path.basename(audio_file_path)}"

    # === CALCULATE DURATIONS ===
    translation_duration = translation_end_time - start_time
    tts_duration = tts_end_time - translation_end_time
    total_duration = tts_end_time - start_time
    
    # Step 4: Return the final JSON response, now including the timing data
    return FullTranslationResponse(
        translated_text=translated_text,
        audio_url=public_audio_url,
        translation_time_seconds=round(translation_duration, 2),
        tts_time_seconds=round(tts_duration, 2),
        total_time_seconds=round(total_duration, 2)
    )