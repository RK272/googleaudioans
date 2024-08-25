from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.helper import voice_input, llm_model_object, text_to_speech,wav_to_pcm,pcm_to_wav,repair
import base64
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
import streamlit as st
from src.helper import voice_input, llm_model_object, text_to_speech

app = FastAPI()

# Mount static files (JavaScript, CSS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process_audio")
async def process_audio(audio: UploadFile = File(...)):
    audio_file_path = "temp_audio.wav"

    with open(audio_file_path, "wb") as buffer:
        buffer.write(await audio.read())

    # Call voice_input function with the audio file path
    #wav_to_pcm(r"D:\multilingual\temp_audio.wav", "output.pcm")
    #pcm_to_wav(r"D:\multilingual\research\output.pcm", "converted_audio.wav")
    repair(r"D:\multilingual\temp_audio.wav", r"D:\multilingual\repaired_audio.wav")
    os.remove(r"D:\multilingual\temp_audio.wav")
    text = voice_input(r"D:\multilingual\repaired_audio.wav")
    os.remove(r"D:\multilingual\repaired_audio.wav")
    print(text)
    response_text = llm_model_object(text)
    print("++++++++++++++")
    print(response_text)

    response_audio_path = "speech.mp3"
    text_to_speech(response_text)

    with open(response_audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()

    # Encode audio to Base64 for JSON response
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

    return JSONResponse(content={"text": response_text, "audio": audio_base64})
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
