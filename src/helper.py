import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import os
import subprocess
#from langchain import ChatPromptTemplate, LLMChain
#from langchain.output_parsers import StringOutputParser

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

#from langchain_core.output_parsers import StringOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

print("perfect!!")
load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY





def voice_input(audio_file_path):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            print("Processing audio file...")
            audio = r.record(source)
            return r.recognize_google(audio)
    except Exception as e:
        print(f"Error: {e}")   

def text_to_speech(text):
    tts=gTTS(text=text, lang="ml")
    
    #save the speech from the given text in the mp3 format
    tts.save("speech.mp3")









def repair(corrupted_file_path, repaired_file_path):
    # Direct path to the FFmpeg executable if it’s in the main folder
    ffmpeg_path = r"D:\multilingual\ffmpeg-2024-08-21-git-9d15fe77e3-full_build\bin\ffmpeg.exe"  # Adjust this path based on where you find ffmpeg.exe

    # Ensure the path is correct, and ffmpeg.exe is in this folder
    if not os.path.isfile(ffmpeg_path):
        raise FileNotFoundError(f"FFmpeg executable not found at path: {ffmpeg_path}")

    # Use FFmpeg to convert corrupted WAV to a repaired WAV
    command = [
        ffmpeg_path, '-i', corrupted_file_path, 
        '-c:a', 'pcm_s16le', '-ar', '44100', '-ac', '2', 
        repaired_file_path
    ]
    try:
        subprocess.run(command, check=True)
        print(f"WAV file repaired and saved to {repaired_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error repairing file: {e}")

# Example usage

    
 





def llm_model_object(user_text):
    # Configure the Google API key
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Initialize the Generative Model
    #llm = genai.GenerativeModel('gemini-1.5-flash')
    llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)
    
    # Define the chat prompt template
    #prompt1 = ChatPromptTemplate.from_template("You are a helpful assistant. Respond to the following input: {user_input}")
    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant you want to answer following qustion in language  they are reffering and strictly 200 tokens and strictly avoid * in output only sentence only pass not pass anything else otherthan sentence .",
        ),
        ("human", "{user_input}"),
    ]
)
    # Create an LLMChain instance with StringOutputParser
    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    
    # Generate the response
   # response = chain.run({'user_input': user_text})
    response=chain.invoke(
    {
        "user_input": user_text,
        
    }
)
    
    return response

    
    
