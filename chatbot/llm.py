import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

class GeminiLLM:
    def _init_(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text