# main.py

import os
import shutil
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles # Import StaticFiles
from app.api.endpoints import translator

# --- Add a cleanup function for old audio files ---
GENERATED_AUDIO_FOLDER = "generated_audio"

def cleanup_audio_folder():
    """Deletes and recreates the audio folder to clear old files."""
    if os.path.exists(GENERATED_AUDIO_FOLDER):
        shutil.rmtree(GENERATED_AUDIO_FOLDER)
    os.makedirs(GENERATED_AUDIO_FOLDER, exist_ok=True)
# -----------------------------------------------

app = FastAPI(
    title="Multilingual Translator API",
    description="A service to translate text and convert it to speech.",
    version="1.0.0"
)

# --- Run cleanup on startup ---
@app.on_event("startup")
async def startup_event():
    cleanup_audio_folder()
# -----------------------------

# --- Mount the static files directory ---
# This makes any file inside 'generated_audio' accessible at the URL '/audio/filename.wav'
app.mount("/audio", StaticFiles(directory=GENERATED_AUDIO_FOLDER), name="audio")
# ---------------------------------------

app.include_router(translator.router, prefix="/api", tags=["Translation"])

@app.get("/")
def read_root():
    """A welcome message for the API root."""
    return {"message": "Welcome to the Multilingual Translator API! Navigate to /docs for the API documentation."}