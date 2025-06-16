# app/api/endpoints/translator.py

import os
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

# Import our two core services
from app.services.translation_service import translate_text
from app.services.tts_service import generate_speech

# Import our Pydantic models
from app.api.models.translator_models import TranslationRequest, FullTranslationResponse

router = APIRouter()

# --- Endpoint 1: The "Real" API for programmatic use ---
@router.post("/translate", response_model=FullTranslationResponse)
async def handle_full_translation_flow(req_body: TranslationRequest, request: Request):
    """
    Translates text, generates speech, and returns a JSON response
    containing the translated text and a public URL to the audio file.
    This is ideal for other applications to use.
    """
    # Step 1: Translate
    translated_text = translate_text(
        source_language=req_body.source_language,
        target_language=req_body.target_language,
        text=req_body.text
    )
    if "Error:" in translated_text:
        raise HTTPException(status_code=500, detail=f"Translation Error: {translated_text}")

    # Step 2: Generate Speech
    audio_file_path = generate_speech(text=translated_text, voice=req_body.voice)
    if "Error:" in audio_file_path:
        raise HTTPException(status_code=500, detail=f"Speech Generation Error: {audio_file_path}")

    # Step 3: Construct the Public URL
    base_url = str(request.base_url)
    public_audio_url = f"{base_url}audio/{os.path.basename(audio_file_path)}"
    
    # Step 4: Return the final JSON response
    return FullTranslationResponse(
        translated_text=translated_text,
        audio_url=public_audio_url
    )




# # --- Endpoint 2: The "Preview" API for Swagger UI Demo ---
# @router.post("/translate/preview", response_class=HTMLResponse)
# async def handle_translate_and_speak_preview(req_body: TranslationRequest, request: Request):
#     """
#     Same as `/translate`, but returns an HTML audio player for easy
#     previewing directly in your browser or the Swagger UI.
#     """
#     # The first part of the logic is identical
#     translated_text = translate_text(
#         source_language=req_body.source_language,
#         target_language=req_body.target_language,
#         text=req_body.text
#     )
#     if "Error:" in translated_text:
#         return HTMLResponse(content=f"<h3>Error during translation:</h3><p>{translated_text}</p>", status_code=500)

#     audio_file_path = generate_speech(text=translated_text, voice=req_body.voice)
#     if "Error:" in audio_file_path:
#         return HTMLResponse(content=f"<h3>Error during speech generation:</h3><p>{audio_file_path}</p>", status_code=500)

#     # Construct the public URL for the audio source
#     base_url = str(request.base_url)
#     audio_url = f"{base_url}audio/{os.path.basename(audio_file_path)}"

    # # Create the HTML content with the translated text and the audio player
    # html_content = f"""
    # <!DOCTYPE html>
    # <html>
    # <head>
    #     <title>Translation Preview</title>
    #     <style>
    #         body {{ font-family: sans-serif; padding: 20px; }}
    #         h3 {{ color: #333; }}
    #         p {{ background-color: #f4f4f4; border-left: 5px solid #ccc; padding: 10px; }}
    #         audio {{ margin-top: 15px; width: 100%; }}
    #     </style>
    # </head>
    # <body>
    #     <h3>Translated Text:</h3>
    #     <p><strong>{translated_text}</strong></p>
        
    #     <h3>Audio Playback:</h3>
    #     <audio controls autoplay>
    #         <source src="{audio_url}" type="audio/wav">
    #         Your browser does not support the audio element.
    #     </audio>
    # </body>
    # </html>
    # """

    # # Return the HTML response
    # return HTMLResponse(content=html_content)

