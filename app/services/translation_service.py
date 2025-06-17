# app/services/translation_service.py

from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY) 

def translate_text(
    source_language: str,
    target_language: str,
    text: str
) -> str:
    """
    Translates text from a source language to a target language using GPT-4o-mini.
    """
    if not text:
        return ""
    
    system_prompt = f"""
    you are an expert multilingual translator. your task is to translate the user's text
    from {source_language} to {target_language}. Your response must contain only the translated 
    text and nothing else. Do not include explanations, apologies, or any other conversational text.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role":"user", "content": text}
            ],
            temperature=0.3,
            max_tokens=1000,
        )
        # THE FIX: Use a different variable name to avoid shadowing the function name.
        translated_text = response.choices[0].message.content.strip()
        return translated_text
        
    except Exception as e:
        print(f"An Error occurred during the OpenAI API call:  {e}")
        return "Error: Could not translate text"