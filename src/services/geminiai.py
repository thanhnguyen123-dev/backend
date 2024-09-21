import google.generativeai as genai
import os
import pytesseract
from PIL import Image
import io


class GoogleGeminiService:
    def __init__(self):
        # Configure the API key for Google Gemini API
        genai.configure(api_key="AIzaSyD6fu5msx3OdVg28EHI89llMYfEjJ0q7Yc")
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate(self, prompt):
        # Use the appropriate method to generate a response from Google Gemini
        response = self.model.generate_content([prompt])
        return response.text 

    def parse_image(self, image_bytes):
        image = Image.open(io.BytesIO(image_bytes))
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text


    #TODO:
    """
    Transcribes an image based on the type of image (prescription or food item)
    Gives the llm a prompt like: "What are the ingrediants"

    For prescription, ask:
        What is the name/s of the medicine?

    You may have to parse the generated response
    Also add the list of prescriptions to the user using add_prescription

    Parameters:
    response (dict): contains an image and an image type 

    Returns:
    generation (dict): response from the llm
        food item example:
        dict = {"type" : "food item",
        "ingrediants": llm_response}

        prescription example:
        {"type" : "prescription",
        "prescriptions" [list of prescriptions]}
    """
    def transcribe_image(self, user, data):
        image_bytes = data.get('image')
        image_type = data.get('type')

        extracted_text = self.parse_image(image_bytes)

        # Build the prompt for LLM based on image type
        string_builder = []
        if image_type == "food_item":
            string_builder.append(f"What are the ingredients of this food item? Here is the text from the image: {extracted_text}")
            string_builder.append(" Return in the dictionary format: {'type': 'food item', 'ingredients': ['ingredient1', 'ingredient2', ...]}")
        elif image_type == "prescription":
            string_builder.append(f"What is the name of the medicine? Here is the text from the prescription: {extracted_text}")
            string_builder.append(" Return in the dictionary format: {'type': 'prescription', 'prescriptions': ['medicine1', 'medicine2', ...]}")

        prompt = "".join(string_builder)

        response = self.generate(prompt)    

        if image_type == "food_item":
            return {"type": "food item", "ingredients": response}
        elif image_type == "prescription":
            user.update_prescriptions(response)
            return {"type": "prescription", "prescriptions": response}
        else:
            return {"error": "Unknown image type"}

    
    """
    Takes an item from the transcribe_image function and queries the LLM
    Use information from the user: allergies, prescriptions and conditions

    Based on the user information and ingrediants list, query the llm if the user can eat this food or worry
    about this prescription

    Parameters:
    user (User): user
    image (dict): response from transcribe_image containing the info about the food item or prescription

    Returns:
    string: LLM response 
    """
    def query_item(self, user, image_data):
        allergies = user.allergies
        prescriptions = user.prescriptions
        conditions = user.conditions
        
        if image_data['type'] == "food item":
            ingredients = image_data['ingredients']
            prompt = f"Can a person with {allergies} allergies eat {ingredients}?"
        elif image_data['type'] == "prescription":
            prescriptions = image_data['prescriptions']
            prompt = f"Can a person with {conditions} conditions take {prescriptions}?"

        response = self.generate(prompt)
        return response
    
    