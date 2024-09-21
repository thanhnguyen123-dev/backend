import google.generativeai as genai
import os
from dotenv import load_dotenv
import pytesseract
from PIL import Image
import io

load_dotenv()

class GoogleGeminiService:
    def __init__(self):
        # Configure the API key for Google Gemini API
        genai.configure(api_key=os.getenv("API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate(self, prompt):
        # Use the appropriate method to generate a response from Google Gemini
        response = self.model.generate_content([prompt])
        return response.text 
    
#TODO:
# def transcribe_image(self, response):
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
    def transcribe_image(self, user, request):
        data = request.get_json()
        image_bytes = data.get('image')
        image_type = data.get('type')

        




        
        string_builder = []
        if image_type == "food_item":
            string_builder.append("What are the ingredients of this food item? ")
            string_builder.append("Return in the dictionary format: {'type': 'food item', 'ingredients': ['ingredient1', 'ingredient2', ...]}")
        elif image_type == "prescription":
            string_builder.append("What is the name of the medicine?")
            string_builder.append("Return in the dictionary format: {'type': 'prescription', 'prescription': ['medicine1', 'medicine2', ...]}")
        
        prompt = "".join(string_builder)
        

        



# def query_food_item(self, user, image):
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
    

    
    