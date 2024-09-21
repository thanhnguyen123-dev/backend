import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleGeminiService:
    def __init__(self):
        # Configure the API key for Google Gemini API
        genai.configure(api_key=os.getenv("API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate(self, prompt):
        # Use the appropriate method to generate a response from Google Gemini
        response = self.model.generate_content([prompt])
        return response.text 
    
    