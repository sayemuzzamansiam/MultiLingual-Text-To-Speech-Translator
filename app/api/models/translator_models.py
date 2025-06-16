# app/api/models/translator_models.py

from pydantic import BaseModel, Field
from typing import Optional

class TranslationRequest(BaseModel):
    """Defines the structure for a translation request."""
    text: str = Field(..., description="The text to be translated.", example="Hello, how are you?")
    source_language: str = Field(..., description="The source language of the text.", example="English")
    target_language: str = Field(..., description="The language to translate the text into.", example="Bangla")
    # Add an optional voice field with a default value
    voice: Optional[str] = Field("Kore", description="The voice to use for speech generation.", example="Puck")

class TranslationResponse(BaseModel):
    """Defines the structure for a simple text-only translation response."""
    translated_text: str

# NEW: Create a response model that includes the audio URL
class FullTranslationResponse(BaseModel):
    """Defines the structure for a full response including translated text and audio URL."""
    translated_text: str
    audio_url: str