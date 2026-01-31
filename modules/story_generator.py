# modules/story_generator.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_story(species_name: str, tone: str = "informative", length: int = 200) -> str:
    """
    Generates a short story or description about a species.

    Args:
        species_name (str): The species to write about.
        tone (str): "informative" or "creative".
        length (int): Approx word count (default=200).

    Returns:
        str: Generated story text.
    """
    prompt = f"""
    Write a {tone.lower()} short story of about {length} words 
    about the species '{species_name}'.
    Include details about its habitat, behaviour, and uniqueness.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Could not generate story. Error: {str(e)}"
