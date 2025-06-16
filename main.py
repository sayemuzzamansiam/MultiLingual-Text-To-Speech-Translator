# Translator/main.py

from fastapi import FastAPI
from app.api.endpoints import translator
from app.api.endpoints import tts  
#Create an instance
app = FastAPI(
    title = "Multilingual Translator API",
    description='A service to translate text and convert it to speech',
    version='1.0.0'
)

# Include the translator router in the main application.
# All endpoints from translator.py will now be available under the /api prefix.

app.include_router(translator.router, prefix="/api",tags=["Translation"])
app.include_router(tts.router, prefix="/api", tags=["Text-to-Speech"])  


@app.get("/")
def read_root():
    {"message": "Welcome to the multilingual Translator"}
    return {"message": "Welcome to the multilingual Translator"} 
