import os
from groq import Groq
import librosa
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from thefuzz import fuzz
import numpy as np

from app.core.config import settings

GENERATED_AUDIO_FOLDER = "generated_audio"
client = Groq(api_key=settings.GROQ_API_KEY)

def _transcribe_audio_with_groq(audio_path: str) -> str:
    """Transcribes audio using Groq's Whisper API."""
    print(f"--- Transcribing audio file: {audio_path}")
    try:
        with open(audio_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(audio_path, file.read()),
                model="whisper-large-v3",
            )
        print(f"--- Groq transcription: '{transcription.text}'")
        return transcription.text
    except Exception as e:
        print(f"--- Error during transcription: {e}")
        return ""

def _calculate_acoustic_similarity(user_audio_path: str, reference_audio_path: str) -> float:
    """Calculates acoustic similarity using MFCC and DTW."""
    try:
        print(f"--- Comparing user audio '{user_audio_path}' with AI audio '{reference_audio_path}'")
        # Load audio files
        y_user, sr_user = librosa.load(user_audio_path)
        y_ref, sr_ref = librosa.load(reference_audio_path)

        # Resample if sample rates are different
        if sr_user != sr_ref:
            y_user = librosa.resample(y=y_user, orig_sr=sr_user, target_sr=sr_ref)

        # Extract MFCCs
        mfcc_user = librosa.feature.mfcc(y=y_user, sr=sr_ref)
        mfcc_ref = librosa.feature.mfcc(y=y_ref, sr=sr_ref)

        # Calculate DTW distance
        distance, _ = fastdtw(mfcc_user.T, mfcc_ref.T, dist=euclidean)

        # Normalize the score (this is empirical and can be tuned)
        # We normalize by the length of the sequences to make it somewhat scale-invariant.
        normalized_distance = distance / (mfcc_user.shape[1] + mfcc_ref.shape[1])

        # Convert distance to a similarity score (0-100). A lower distance means higher similarity.
        # The scaling factor of 10 is chosen empirically. A larger factor makes the score drop faster.
        score = max(0, 100 - (normalized_distance * 10))

        print(f"--- DTW Distance: {distance:.2f}, Normalized: {normalized_distance:.2f}, Acoustic Score: {score:.2f}")
        return round(score, 2)

    except Exception as e:
        print(f"--- Error during acoustic comparison: {e}")
        return 0.0


def score_pronunciation(user_audio_path: str, reference_audio_path: str, reference_text: str) -> dict:
    """
    Orchestrates the pronunciation scoring process.
    """
    # 1. Intelligibility Score (Did they say the right words?)
    transcribed_text = _transcribe_audio_with_groq(user_audio_path)
    if not transcribed_text:
        intelligibility_score = 0.0
    else:
        # Use fuzzy string matching to score
        intelligibility_score = fuzz.ratio(reference_text.lower(), transcribed_text.lower())

    # 2. Acoustic Similarity Score (Did they sound like the AI?)
    if not os.path.exists(reference_audio_path):
        print(f"--- Reference audio not found at: {reference_audio_path}")
        acoustic_similarity_score = 0.0
    else:
        acoustic_similarity_score = _calculate_acoustic_similarity(user_audio_path, reference_audio_path)

    # 3. Overall Score (Weighted average)
    # We weigh intelligibility higher because saying the right words is most important.
    overall_score = (0.65 * intelligibility_score) + (0.35 * acoustic_similarity_score)

    return {
        "reference_text": reference_text,
        "transcribed_text": transcribed_text if transcribed_text else "Could not transcribe audio.",
        "intelligibility_score": round(intelligibility_score, 2),
        "acoustic_similarity_score": round(acoustic_similarity_score, 2),
        "overall_score": round(overall_score, 2)
    }