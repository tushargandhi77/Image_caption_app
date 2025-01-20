import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def generate_captions(image_path, platform, num_captions):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are a creative expert in generating positive and engaging captions for images. 
    Based on the uploaded image, create {num_captions} unique, platform-specific captions 
    suitable for {platform}. Ensure the captions are positive, inspiring, and align with 
    the theme of the image.
    """
    
    with open(image_path, 'rb') as img_file:
        image_data = [{"mime_type": "image/jpeg", "data": img_file.read()}]
    
    response = model.generate_content([prompt, image_data[0]])
    return response.text