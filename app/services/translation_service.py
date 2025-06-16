
#app/services/translation_service.py

from openai import OpenAI
from app.core.config import settings

#instantiate the openai client with the API key from out settings

#it'll automatically read the api key environment variable if not passed directly

client = OpenAI(api_key=settings.OPENAI_API_KEY) 

def translate_text(
    source_language: str,
    target_language: str,
    text: str
)->str:
    """    Translates text from a source language to a target language using GPT-4o-mini.

    Args:
        source_language: The language of the input text (e.g., "English").
        target_language: The language to translate to (e.g., "Japanese").
        text: The text to be translated.

    Returns:
        The translated text as a string.

    """
    if not text:
        return ""
    

    # we will create system prompt which is important for steering the model's behavior
    # it instructs the LLM to act as  professional translator and return only the translated text
    
    system_prompt = f"""
    you are an expert multilingual translator. your task is to translate the user's text
    from {source_language} to {target_language}. Your response must contain only the translated 
    text and nothing else. Do not include explanations, apologies, or any other conversational text.
    """
    
    # making the api call:
    try:
        response = client.chat.completions.create( # it also has client.embedding, image,audio we can use em.
            model = "gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role":"user", "content": text}
            ],
            temperature=0.3, #lower temp for more deterministic, factual translations
            max_tokens=1000,
        ) # this is the main func. call that sends the request to the OpenAI API.
        translate_text = response.choices[0].message.content.strip()
        return translate_text
    except Exception as e:
        print(f"An Error occurred during the OpenAI API call:  {e}")
        return "Error: Could not translated text"
    
    
    