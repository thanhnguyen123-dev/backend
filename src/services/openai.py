import openai
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()


class OpenAIService:
    def __init__(self, api_key):
        openai.api_key = api_key

    def get_response(self, prompt):
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()

# Example usage
if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    service = OpenAIService(api_key)
    prompt = "Once upon a time"
    generated_text = service.generate_text(prompt)
    print(generated_text)