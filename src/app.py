import os
from flask import Flask, request, jsonify
from services.geminiai import GoogleGeminiService
from dotenv import load_dotenv
import requests

import json
import base64
from io import BytesIO
from PIL import Image

from users import UserManager, User

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("API_KEY") #gemini

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_INTERNAL_SERVER_ERROR = 500
users = {}

user_manager = UserManager()



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

@app.route('/user', methods=['POST', 'GET', 'PUT'])
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
        data = request.get_json()
        user_id = data['user_id']
        user: User = user_manager.get_user(user_id)
        return jsonify({"status": "success", "users": user.to_dict()}), HTTP_OK
    
    elif request.method == 'PUT':
        data = request.get_json()  # Get JSON data from the request
        user_id = data.get('user_id')
        
        if user_id and all(key in data for key in ['name', 'age', 'allergies', 'conditions', 'prescriptions']):
            user_info = user_manager.update_user(user_id, data)  # Assuming you have an update_user method
            user = user_info.to_dict()
            print(f"User updated: {user_info}")
            return jsonify({"status": "success", "user": user}), 200  # Use HTTP_OK constant if defined
        else:
            return jsonify({"status": "error", "message": "Invalid"}), 400  # Use HTTP_BAD_REQUEST constant if defined



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
@app.route('/api/query_image/<user_id>', methods=['POST'])
def query_image(user_id):
    data = request.json
    if 'image' not in data or 'type' not in data:
        return jsonify({'error': 'Image data and type are required'}), 400
    
    try:
        # Decode the base64 string
        img_data = base64.b64decode(data['image'])
        
        # Prepare the data for transcribe_image
        image_data = {
            'image': img_data,
            'type': data['type']
        }
        
        # Process the image
        user = user_manager.get_user(user_id)
        transcribed_data = gemini_service.transcribe_image(user, image_data)
        response = gemini_service.query_item(user, transcribed_data)
        
        if response:
            return jsonify({'response': response}), 200
        else:
            return jsonify({'error': 'Unable to generate response'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/query_barcode/<user_id>', methods=['POST'])
def query_barcode(user_id):
    # Get the barcode from the request JSON
    data = request.get_json()
    barcode = data['barcode']

    if not barcode:
        return jsonify({"error": "Barcode is required"}), 400
    
    # URL of the product
    url = f"https://world.openfoodfacts.net/api/v2/product/{barcode}"

    # Make the GET request
    response = requests.get(url)

    item_data = {"type": "food item"}

    # Check if the request was successful
    if response.status_code == 200:
        product_data = response.json()  # Parse JSON response
        ingredients_text = product_data.get('product', {}).get('ingredients_text', 'No ingredients found.')
        ingredients_list = [ingredient.strip() for ingredient in ingredients_text.split(',')]
        item_data["ingredients"] = ingredients_list
    else:
        return f"Failed to retrieve product data: {response.status_code}"
    
    user: User = user_manager.get_user(1)
    response: str = gemini_service.query_item(user, item_data)
    
    if response:
        return jsonify({'response': response}), HTTP_OK
    else:
        return jsonify({'error': 'Unable to generate response'}), 


@app.route('/api/recipes/<user_id>', methods=['GET'])
def recipes(user_id):
    user: User = user_manager.get_user(user_id)
    response: str = gemini_service.generate_recipes(user)

    if response:
        return jsonify({'response': response}), HTTP_OK
    else:
        return jsonify({'error': 'Unable to generate response'}), 

@app.route('/api/dietary_restrictions/<user_id>', methods=['GET'])
def dietary_restrictions(user_id):
    user: User = user_manager.get_user(user_id)
    response: str = gemini_service.get_dietary_restrictions(user)

    if response:
        return jsonify({'response': response}), HTTP_OK
    else:
        return jsonify({'error': 'Unable to generate response'}), 


if __name__ == '__main__':
    app.run(debug=True)
