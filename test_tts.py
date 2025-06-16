# test_tts.py
from app.services.tts_service import generate_speech
import os

def run_final_test():
    print("--- Running Final TTS Test with User-Provided Logic ---")

    # Test with English text
    english_text = "This is the final test. I am confident it will work this time."
    returned_path_en = generate_speech(english_text, voice="Puck")
    
    # Check if the file was created
    if os.path.exists(returned_path_en):
        print(f"SUCCESS: English audio file created at: {returned_path_en}")
    else:
        print(f"FAILURE: Could not create English audio file. Service response: {returned_path_en}")

    print("-" * 30)

    # Test with Japanese text
    japanese_text = "こんにちは世界、これは最後のテストです。"
    returned_path_jp = generate_speech(japanese_text, voice="Kore")

    if os.path.exists(returned_path_jp):
        print(f"SUCCESS: Japanese audio file created at: {returned_path_jp}")
    else:
        print(f"FAILURE: Could not create Japanese audio file. Service response: {returned_path_jp}")


if __name__ == "__main__":
    run_final_test()