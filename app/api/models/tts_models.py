
# translator/app/models/tts_models.py
from pydantic import BaseModel, Field

class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to convert into speech", example="Hello, how are you?")
    voice: str = Field(default="Kore", description="Voice to use for speech synthesis", example="Leda")

class TTSResponse(BaseModel):
    audio_file_path: str
