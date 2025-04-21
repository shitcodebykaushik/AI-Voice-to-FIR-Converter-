import whisper
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Load API Key
genai.configure(api_key='AIzaSyBZ9L6u7RVJtN-U2mPOZXeMT8UEQbIgPmQ')

# whisper_model = whisper.load_model("base")


def audio_to_text(audio_path):
    """ Converts audio file to text using Whisper """
    # Load the Whisper model only when needed
    whisper_model = whisper.load_model("tiny")
    result = whisper_model.transcribe(audio_path)
    return result["text"]


def generate_fir(transcribed_text):
    """ Uses Gemini AI to generate a structured and legally accurate FIR """
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    You are an expert in legal documentation and law enforcement reporting. 
    Your task is to generate a **proper FIR (First Information Report)** based on the given complaint.
    
    - **Remove any police voice or irrelevant speech** and extract only the victim’s statement.
    - **Analyze the complaint and determine applicable IPC (Indian Penal Code) sections** for the crime.
    - **Ensure the FIR follows official legal format** with proper structure.
    - **Highlight missing details** that should be added during investigation.
    
    Complaint Text (extract only useful parts and generate FIR accordingly):  
    '''{transcribed_text}'''

    Now generate a structured **FIR document** as per legal guidelines.
    """

    response = model.generate_content(prompt)
    return response.text
