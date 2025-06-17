# app/api/models/translator_models.py

from pydantic import BaseModel, Field
from typing import Optional

class TranslationRequest(BaseModel):
    """Defines the structure for a translation request."""
    text: str = Field(..., description="The text to be translated.", example="Hello, how are you?")
    source_language: str = Field(..., description="The source language of the text.", example="English")
    target_language: str = Field(..., description="The language to translate the text into.", example="Bangla")
    voice: Optional[str] = Field("Kore", description="The voice to use for speech generation.", example="Puck")

# THE FIX: Consolidate the duplicate class into one final, correct definition.
class FullTranslationResponse(BaseModel):
    """Defines the structure for a full response including text, audio URL, and timing."""
    translated_text: str
    audio_url: str
    translation_time_seconds: Optional[float] = None
    tts_time_seconds: Optional[float] = None
    total_time_seconds: Optional[float] = None