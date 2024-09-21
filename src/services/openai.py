from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class OpenAIService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

    def generate_text(self, prompt):
        response = self.client.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    

