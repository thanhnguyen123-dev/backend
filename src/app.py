import os
from flask import Flask, request, jsonify
from services.openai import OpenAIService
from dotenv import load_dotenv

import json

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")

HTTP_OK = 200
HTTP_BAD_REQUEST = 400

openai = OpenAIService(api_key)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api')
def api():
    return "Hello, API!"

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'prompt is required'}), HTTP_BAD_REQUEST
    response = openai.generate_text(prompt)
    return jsonify({'response': response}), HTTP_OK
