import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.api.models.pronunciation_models import PronunciationScoreResponse
from app.services.pronunciation_service import score_pronunciation

router = APIRouter()

GENERATED_AUDIO_FOLDER = "generated_audio"
TEMP_FOLDER = "temp_audio"
os.makedirs(TEMP_FOLDER, exist_ok=True)

@router.post("/pronunciation-check", response_model=PronunciationScoreResponse, tags=["Pronunciation"])
async def handle_pronunciation_check(
    user_audio: UploadFile = File(..., description="The user's recorded audio file (WAV)."),
    reference_filename: str = Form(..., description="The filename of the AI-generated audio to compare against."),
    reference_text: str = Form(..., description="The correct text phrase for the audio.")
):
    """
    Analyzes user's pronunciation by comparing their audio to a reference AI audio.

    - Transcribes the user's audio for an **intelligibility score**.
    - Compares audio features (MFCCs) for an **acoustic similarity score**.
    - Returns a combined **overall score**.
    """
    # 1. Save the uploaded user audio to a temporary file
    temp_id = uuid.uuid4()
    temp_user_audio_path = os.path.join(TEMP_FOLDER, f"user_{temp_id}.wav")

    try:
        with open(temp_user_audio_path, "wb") as buffer:
            shutil.copyfileobj(user_audio.file, buffer)
    finally:
        user_audio.file.close()

    # 2. Locate the reference audio file
    reference_audio_path = os.path.join(GENERATED_AUDIO_FOLDER, reference_filename)
    if not os.path.exists(reference_audio_path):
        os.remove(temp_user_audio_path) # Clean up temp file
        raise HTTPException(status_code=404, detail=f"Reference audio file '{reference_filename}' not found.")

    # 3. Call the scoring service
    try:
        score_data = score_pronunciation(
            user_audio_path=temp_user_audio_path,
            reference_audio_path=reference_audio_path,
            reference_text=reference_text
        )
        return PronunciationScoreResponse(**score_data)
    except Exception as e:
        # Catch any unexpected errors from the service
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 4. Clean up the temporary user audio file
        if os.path.exists(temp_user_audio_path):
            os.remove(temp_user_audio_path)