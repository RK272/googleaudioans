import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
import streamlit as st
from src.helper import voice_input, llm_model_object, text_to_speech

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

def voice_input():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("You said: ", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio")
    except sr.RequestError as e:
        print("Could not request result from Google Speech Recognition service: {0}".format(e))

def text_to_speech(text, gender='neutral', language_code='ml-IN'):
    """
    Convert text to speech with different voice styles.

    Args:
    text (str): The text to convert to speech.
    gender (str): The gender of the voice ('neutral', 'male', 'female').
    language_code (str): The language code (e.g., 'en-US' for English, 'ml-IN' for Malayalam).
    """
    # Initialize a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Set the voice parameters
    gender_map = {
        'neutral': texttospeech.SsmlVoiceGender.NEUTRAL,
        'male': texttospeech.SsmlVoiceGender.MALE,
        'female': texttospeech.SsmlVoiceGender.FEMALE
    }

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=gender_map.get(gender, texttospeech.SsmlVoiceGender.NEUTRAL)
    )

    # Set the audio configuration
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Save the audio to a file
    with open("speech.mp3", "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file 'speech.mp3'")

def llm_model_object(user_text):
    # Configure the generative model
    genai.configure(api_key=GOOGLE_API_KEY)
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    response = model.generate_content(user_text)
    
    result = response.text
    
    return result

# Example usage:
user_input = voice_input()
if user_input:
    response_text = llm_model_object(user_input)
    text_to_speech(response_text, gender='female', language_code='ml-IN')
