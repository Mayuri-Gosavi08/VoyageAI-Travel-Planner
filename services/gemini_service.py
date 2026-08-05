import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Read API Key from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Gemini API Key not found. Check your .env file.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-flash-latest")
def generate_response(prompt: str):
    """
    Sends a prompt to Gemini AI and returns the response.
    """
    response = model.generate_content(prompt)
    return response.text