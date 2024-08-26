from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.helper import voice_input, llm_model_object, text_to_speech,repair
import base64
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os

from src.helper import voice_input, llm_model_object, text_to_speech
from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import base64
import os

app = FastAPI()

# Mount static files (JavaScript, CSS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_home(request: Request):
    return templates.TemplateResponse("index1.html", {"request": request})

@app.post("/process_text")
async def process_text(text: str = Form(...)):
    # Process the text input
    print("Received text:", text)
    
    # Call your model or processing function here
    response_text = llm_model_object(text)
    print("Processed response:", response_text)

    # For demonstration, if you need to return audio as well
    response_audio_path = "speech.mp3"
    text_to_speech(response_text)

    with open(response_audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()

    # Encode audio to Base64 for JSON response
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

    return JSONResponse(content={"text": response_text, "audio": audio_base64})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
