import os
from flask import Flask, request, jsonify
from services.geminiai import GoogleGeminiService
from dotenv import load_dotenv

import json

from users import UserManager
import services.geminiai

api_key = os.getenv("API_KEY") #gemini

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
users = {}

user_manager = UserManager()

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

@app.route('/user', methods=['POST'])
def receive_message():
    data = request.get_json()  # Get JSON data from the request
    if data and all(key in data for key in ['name', 'age', 'allergies', 'conditions']):
        user_info = user_manager.add_user(data)  
        print(f"User added: {user_info}")
        return jsonify({"status": "success", "user": user_info}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid"}), 400


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

#request: {"image": imagefile,
#           "type":  "prescription/food_item"}
# call function to transcribe image into text 
@app.route('/api/query_image', methods=['POST'])
def query_image():
    return None

if __name__ == '__main__':
    app.run(debug=True)
