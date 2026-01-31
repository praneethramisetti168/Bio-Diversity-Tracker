# modules/map_utils.py

import requests
import os
from dotenv import load_dotenv
import streamlit as st

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def get_coordinates(location_name: str):
    """
    Convert a location string (e.g., 'India') to (lat, lon) using Google Geocoding API.
    Fallbacks to None if request fails.
    """
    if not location_name:
        return None, None

    if not GOOGLE_API_KEY:
        st.warning("GOOGLE_API_KEY not found in environment")
        return None, None

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": location_name, "key": GOOGLE_API_KEY}

    try:
        response = requests.get(url, params=params).json()
    except Exception as e:
        st.error(f"Error contacting Google Geocoding API: {e}")
        return None, None

    # Debug info
    st.write("Google API Response Status:", response.get("status"))

    if response.get("status") == "OK":
        lat = response["results"][0]["geometry"]["location"]["lat"]
        lng = response["results"][0]["geometry"]["location"]["lng"]
        return lat, lng
    else:
        return None, None


def generate_map_iframe(lat: float, lon: float, zoom: int = 4) -> str:
    """
    Creates an embeddable Google Maps iframe centered on given coordinates.
    """
    if not lat or not lon:
        return "<p>Could not fetch map location</p>"

    iframe = f"""
    <iframe
      width="100%"
      height="350"
      style="border:0"
      loading="lazy"
      allowfullscreen
      referrerpolicy="no-referrer-when-downgrade"
      src="https://www.google.com/maps/embed/v1/view?key={GOOGLE_API_KEY}&center={lat},{lon}&zoom={zoom}&maptype=roadmap">
    </iframe>
    """
    return iframe