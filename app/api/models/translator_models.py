# app/api/models/translator_models.py

from pydantic import BaseModel, Field

class TranslationRequest(BaseModel):
    """
    Define the structure for a translation request.
    
    """
    text: str = Field(..., example="hello how are you?")
    source_language: str = Field(..., example="English")
    target_language: str = Field(..., example="Bangla")
    voice: str = Field(default="Kore", example="Kore")
    
class TranslationResponse(BaseModel):
    """ define the structure for a translation response
    """
    translated_text: str
    audio_file_path: str
