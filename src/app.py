import os
from flask import Flask, request, jsonify
from services.geminiai import GoogleGeminiService
from dotenv import load_dotenv

import json

HTTP_OK = 200
HTTP_BAD_REQUEST = 400

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Create an instance of the GoogleGeminiService
gemini_service = GoogleGeminiService()

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api')
def api():
    return "Hello, API!"

@app.route('/api/generate', methods=['POST'])
def generate():
    # Get the prompt from the request body
    prompt = request.json.get('prompt')

    # Check if the prompt is missing
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), HTTP_BAD_REQUEST

    # Generate a response using the Google Gemini service
    response = gemini_service.generate(prompt)
    print(response['response'])

    # Return the response as JSON
    return jsonify({'response': response}), HTTP_OK


if __name__ == '__main__':
    app.run(debug=True)
