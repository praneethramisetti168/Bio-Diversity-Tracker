# modules/species_info.py

import re
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


def get_species_info(species_name: str) -> dict:
    """
    Fetches scientific name, common name, habitat, distribution,
    and conservation status of a species using Gemini API.
    """
    prompt = f"""
    You are a biodiversity expert. 
    Respond ONLY in valid JSON (no text outside JSON).
    Keys required:
    scientific_name, common_name, habitat, distribution, conservation_status.
    Example:
    {{
      "scientific_name": "Panthera tigris tigris",
      "common_name": "Bengal Tiger",
      "habitat": "Tropical rainforests, grasslands, mangroves",
      "distribution": "India, Bangladesh, Bhutan, Nepal",
      "conservation_status": "Endangered"
    }}
    Species: "{species_name}"
    """

    try:
        response = model.generate_content(prompt)

        # Extract text safely
        text_response = response.candidates[0].content.parts[0].text.strip()
        text_response = re.sub(r"```json|```", "", text_response).strip()

        info = json.loads(text_response)
        return info

    except Exception as e:
        return {
            "scientific_name": None,
            "common_name": species_name,
            "habitat": "Unknown",
            "distribution": "Unknown",
            "conservation_status": "Unknown",
            "error": str(e)
        }
