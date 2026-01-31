# app.py

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from modules.species_info import get_species_info
from modules.map_utils import get_coordinates, generate_map_iframe
from modules.story_generator import generate_story
from modules.chatbot import chat_about_species

st.set_page_config(page_title="🌿 Biodiversity Tracker", layout="wide")
st.title("🌿 Biodiversity Tracker with Story Generation")

# Sidebar
st.sidebar.header("Settings")
tone = st.sidebar.radio("Story Tone", ["Informative", "Creative"])
length = st.sidebar.slider("Story Length (words)", 100, 500, 200)

# User input
species_name = st.text_input("🔍 Enter species name (e.g., Bengal Tiger):")

if species_name:
    # ----------------- Species Info -----------------
    with st.spinner("Fetching species information..."):
        info = get_species_info(species_name)

    st.subheader("🔬 Species Information")
    st.json(info)

    # ----------------- Map -----------------
    st.subheader("🌍 Global Distribution")
    distribution = info.get("distribution", "")
    if distribution:
        first_location = distribution.split(",")[0].strip()  # pick first country/region
        lat, lon = get_coordinates(first_location)
        iframe = generate_map_iframe(lat, lon)
    else:
        iframe = "<p>Could not fetch map location</p>"

    st.components.v1.html(iframe, height=350)

    # ----------------- Story -----------------
    st.subheader("📖 Generated Story")
    if "story" not in st.session_state:
        st.session_state.story = None

    if st.button("Generate Story"):
        st.session_state.story = generate_story(species_name, tone=tone, length=length)

    if st.session_state.story:
        st.write(st.session_state.story)

    # ----------------- Chatbot -----------------
    st.subheader("💬 Ask the Assistant")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_question = st.text_input("Your question about this species:")

    if st.button("Ask"):
        answer, updated_history = chat_about_species(
            species_name, user_question, st.session_state.chat_history
        )
        st.session_state.chat_history = updated_history

    # Display chat
    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**Assistant:** {msg}")
