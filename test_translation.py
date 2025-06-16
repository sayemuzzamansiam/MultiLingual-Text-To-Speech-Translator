# translator/test_translation.py

from app.services.translation_service import translate_text

def run_test():
    """ 
        Runs a simple test to check the translation func.
    """
    
    print("====== Start Translation Test ========")
    
    source_lang_1 = "English"
    target_lang_1 = "Bangla"
    text_to_translate_1 = "Hello my name is Sam Mahmud. I am the strongest worrier of the ancient era"
    
    print(f"\nTranslating from {source_lang_1} to {target_lang_1}...")
    print(f"Input Text: {text_to_translate_1}")
    
    text_to_translate_1 = translate_text(
        source_language=source_lang_1,
        target_language=target_lang_1,
        text=text_to_translate_1
    )
    
    print(f"Translated Output  {text_to_translate_1}")
    print("-" * 20)
    
    
    
        # --- Test Case 2: Hindi to German ---
    source_lang_2 = "Hindi"
    target_lang_2 = "German"
    text_to_translate_2 = "आपका दिन कैसा रहा?" # (How was your day?)

    print(f"\nTranslating from {source_lang_2} to {target_lang_2}...")
    print(f"Input Text: {text_to_translate_2}")

    translated_text_2 = translate_text(
        source_language=source_lang_2,
        target_language=target_lang_2,
        text=text_to_translate_2
    )

    print(f"Translated Output: {translated_text_2}")
    print("-" * 20)

    print("\n--- Translation Test Finished ---")


if __name__ == "__main__":
    
    run_test()
