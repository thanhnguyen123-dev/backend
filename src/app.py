import os
from flask import Flask, request, jsonify
from services.geminiai import GoogleGeminiService
from dotenv import load_dotenv

import json

from users import UserManager, User
import services.geminiai as geminiai

api_key = os.getenv("API_KEY") #gemini

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_INTERNAL_SERVER_ERROR = 500
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

@app.route('/user', methods=['POST', 'GET'])
def user_route():
    if request.method == 'POST':
        data = request.get_json()  # Get JSON data from the request
        if data and all(key in data for key in ['name', 'age', 'allergies', 'conditions', 'prescriptions']):
            user_info = user_manager.add_user(data)
            user = user_info.to_dict()  
            print(f"User added: {user_info}")
            return jsonify({"status": "success", "user": user}), HTTP_OK
        else:
            return jsonify({"status": "error", "message": "Invalid"}), HTTP_BAD_REQUEST

    elif request.method == 'GET':
        user: User = user_manager.get_user(1)
        return jsonify({"status": "success", "users": user.to_dict()}), HTTP_OK


@app.route('/api/generate', methods=['POST'])
def generate():
    # Get the prompt from the request body
    prompt = request.json.get('prompt')

    # Check if the prompt is missing
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), HTTP_BAD_REQUEST

    # Generate a response using the Google Gemini service
    response = gemini_service.generate(prompt)

    # Return the response as JSON
    return jsonify({'response': response}), HTTP_OK

#request: {"image": imagefile,
#           "type":  "prescription/food_item"}
# call function to transcribe image into text 
@app.route('/api/query_image', methods=['POST'])
def query_image():
    data: dict = request.get_json()
    user: User = user_manager.get_user(1)
    image_data: dict = geminiai.transcribe_image(user, data)

    response: str = geminiai.query_item(user, image_data)
    
    if response:
        return jsonify({'response': response}), HTTP_OK
    else:
        return jsonify({'error': 'Unable to generate response'}), 

@app.route('/api/recipes', methods=['GET'])
def recipes():
    user: User = user_manager.get_user(1)
    response: str = geminiai.generate_recipes(user)

    if response:
        return jsonify({'response': response}), HTTP_OK
    else:
        return jsonify({'error': 'Unable to generate response'}), 

@app.route('/api/dietary_restrictions', methods=['GET'])
def dietary_restrictions():
    user: User = user_manager.get_user(1)
    response: str = geminiai.get_dietary_restrictions(user)

    if response:
        return jsonify({'response': response}), HTTP_OK
    else:
        return jsonify({'error': 'Unable to generate response'}), 


if __name__ == '__main__':
    app.run(debug=True)
