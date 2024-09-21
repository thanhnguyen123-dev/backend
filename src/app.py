import os
from flask import Flask, request, jsonify
from services.openai import OpenAIService
from dotenv import load_dotenv
import uuid

import json

from users import UserManager

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("API_KEY") #gemini

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
users = {}

openai = OpenAIService(api_key)
user_manager = UserManager()

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api')
def api():
    return "Hello, API!"

@app.route('/user', methods=['POST'])
def receive_message():
    data = request.get_json()  # Get JSON data from the request
    if data and all(key in data for key in ['name', 'age', 'allergies', 'conditions']):
        user_info = user_manager.add_user(data)  
        print(f"User added: {user_info}")
        return jsonify({"status": "success", "user": user_info}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid"}), 400

@app.route('/user/prescription', methods=[])


@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'prompt is required'}), HTTP_BAD_REQUEST
    response = openai.generate_text(prompt)
    return jsonify({'response': response}), HTTP_OK
