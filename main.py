import os
import shutil
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Import all endpoint routers
from app.api.endpoints import translator, pronunciation

GENERATED_AUDIO_FOLDER = "generated_audio"

def cleanup_audio_folder():
    """Deletes and recreates the audio folder to clear old files."""
    if os.path.exists(GENERATED_AUDIO_FOLDER):
        shutil.rmtree(GENERATED_AUDIO_FOLDER)
    os.makedirs(GENERATED_AUDIO_FOLDER, exist_ok=True)

app = FastAPI(
    title="Multilingual Translator & Pronunciation Coach API",
    description="A service to translate text, convert it to speech, and score user pronunciation.",
    version="2.0.0"
)

@app.on_event("startup")
async def startup_event():
    cleanup_audio_folder()

# Mount the static files directory for serving generated audio
app.mount("/audio", StaticFiles(directory=GENERATED_AUDIO_FOLDER), name="audio")

# Include all API routers
app.include_router(translator.router, prefix="/api", tags=["Translation"])
app.include_router(pronunciation.router, prefix="/api", tags=["Pronunciation"]) # Add this line

@app.get("/")
def read_root():
    """A welcome message for the API root."""
    return {"message": "Welcome to the API! Navigate to /docs for documentation."}