import requests
import pyaudio
import wave
import os
import time
import sys

# --- Configuration ---
API_BASE_URL = "http://127.0.0.1:8000"
TRANSLATE_URL = f"{API_BASE_URL}/api/translate"
PRONUNCIATION_URL = f"{API_BASE_URL}/api/pronunciation-check"

# PyAudio Configuration
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "user_audio.wav"
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000 # Sample rate for recording

def record_audio():
    """Records audio from the microphone for a fixed duration."""
    p = pyaudio.PyAudio()

    print(f"\n--- Please get ready to speak. Recording will start in 3 seconds...")
    time.sleep(3)
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print(f"--- RECORDING for {RECORD_SECONDS} seconds... Speak now! ---")

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("--- Recording complete. ---")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"--- Your audio has been saved to '{WAVE_OUTPUT_FILENAME}' ---")


def get_translation_and_ai_audio(text, source_lang, target_lang):
    """Calls the translation endpoint."""
    print("\n>>> Contacting server for translation and AI audio...")
    payload = {
        "text": text,
        "source_language": source_lang,
        "target_language": target_lang
    }
    try:
        response = requests.post(TRANSLATE_URL, json=payload)
        response.raise_for_status() # Raises an exception for 4XX/5XX errors
        data = response.json()
        translated_text = data.get("translated_text")
        audio_url = data.get("audio_url")
        # Extract filename from URL
        reference_filename = audio_url.split('/')[-1]
        return translated_text, reference_filename
    except requests.exceptions.RequestException as e:
        print(f"!!! ERROR: Could not connect to the server: {e}", file=sys.stderr)
        return None, None

def get_pronunciation_score(audio_path, ref_filename, ref_text):
    """Calls the pronunciation scoring endpoint."""
    print(">>> Uploading your audio for analysis...")
    with open(audio_path, 'rb') as f:
        files = {'user_audio': (audio_path, f, 'audio/wav')}
        data = {
            'reference_filename': ref_filename,
            'reference_text': ref_text
        }
        try:
            response = requests.post(PRONUNCIATION_URL, files=files, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"!!! ERROR: Could not get score from server: {e}", file=sys.stderr)
            print(f"Server response: {response.text}", file=sys.stderr)
            return None


def main():
    """Main execution flow for the client."""
    print("--- Welcome to the Pronunciation Coach Client ---")
    
    # Step 1: Get user input for translation
    text_to_translate = input("Enter the text you want to practice: ")
    source_language = input("Enter the source language (e.g., 'English'): ")
    target_language = input("Enter the target language (e.g., 'Bangla'): ")

    # Step 2: Get translation and AI audio reference
    translated_text, ref_filename = get_translation_and_ai_audio(
        text_to_translate, source_language, target_language
    )
    if not translated_text:
        return # Exit if translation fails

    print("\n========================================================")
    print(f"AI Translation: '{translated_text}'")
    print("Listen to the AI's pronunciation (you can find the audio file on the server).")
    print("========================================================")

    # Step 3: Record user's audio
    record_audio()

    # Step 4: Get pronunciation score
    score_data = get_pronunciation_score(WAVE_OUTPUT_FILENAME, ref_filename, translated_text)

    # Step 5: Display results and clean up
    if score_data:
        print("\n--- Your Pronunciation Report ---")
        print(f"  Reference Text: '{score_data['reference_text']}'")
        print(f"     Machine Heard: '{score_data['transcribed_text']}'")
        print("-----------------------------------")
        print(f"  Clarity Score (Words):    {score_data['intelligibility_score']:.2f} / 100")
        print(f"  Accent Score (Sound):     {score_data['acoustic_similarity_score']:.2f} / 100")
        print("-----------------------------------")
        print(f"  OVERALL SCORE:            {score_data['overall_score']:.2f} / 100")
        print("-----------------------------------\n")

    if os.path.exists(WAVE_OUTPUT_FILENAME):
        os.remove(WAVE_OUTPUT_FILENAME)
        print(f"--- Cleaned up temporary file: '{WAVE_OUTPUT_FILENAME}' ---")


if __name__ == "__main__":
    main()