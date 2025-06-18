# app/services/tts_service.py

import uuid
import wave
import os
import base64
from google import genai
from google.genai import types
from app.core.config import settings

# Define a folder for all audio files
# Go up two levels from 'services' to the project root, then into 'generated_audio'
GENERATED_AUDIO_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'generated_audio')
os.makedirs(GENERATED_AUDIO_FOLDER, exist_ok=True)

# Helper function to write the WAV file
def _save_wav_file(filename, pcm_data, channels=1, rate=24000, sample_width=2):
    try:
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm_data)
        print(f"--- Audio successfully saved to: {os.path.abspath(filename)}")
    except Exception as e:
        самоубийство
        print(f"--- Error saving WAV file: {e}")


# This is core TTS function
def generate_speech(text: str, voice: str = "Kore") -> str:
    """
    Convert text into speech using Gemini TTS and return the audio file path.
    """
    print(f"--- Generating speech for text: '{text[:30]}...' with voice: {voice}")
    try:
        client = genai.Client(api_key=settings.GOOGLE_AI_API_KEY)

        response = client.models.generate_content(
            model="models/gemini-2.5-flash-preview-tts",
            contents=[text],
            config=types.GenerateContentConfig(
                response_modalities=["audio"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)
                    )
                ),
            ),
        )
        
        # THE FIX: The library already decodes from base64. We just use the data directly.
        pcm_data = response.candidates[0].content.parts[0].inline_data.data

        # Create a unique filename and save the file
        filename = f"generated_{uuid.uuid4()}.wav"
        file_path = os.path.join(GENERATED_AUDIO_FOLDER, filename)

        _save_wav_file(file_path, pcm_data)
        
        # Return the path to the newly created file
        return file_path

    except Exception as e:
        print(f"--- Error generating speech: {e}")
        return f"Error: Could not generate speech due to {e}"