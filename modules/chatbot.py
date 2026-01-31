# modules/chatbot.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


def chat_about_species(species_name: str, user_question: str, chat_history: list) -> tuple:
    """
    Chatbot function to answer user questions about a given species.

    Args:
        species_name (str): The species being discussed.
        user_question (str): User's current query.
        chat_history (list): Previous conversation history as list of (role, message).

    Returns:
        tuple: (assistant_response, updated_chat_history)
    """
    # Build context from history
    history_text = "\n".join([f"{role.upper()}: {msg}" for role, msg in chat_history])

    prompt = f"""
    You are a friendly naturalist assistant.
    The user is asking about the species '{species_name}'.
    
    Chat so far:
    {history_text}

    User's new question: {user_question}

    Please give a concise and helpful answer (max 4-5 sentences).
    """

    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()
        # update history
        chat_history.append(("user", user_question))
        chat_history.append(("assistant", answer))
        return answer, chat_history
    except Exception as e:
        error_msg = f"⚠️ Could not generate response. Error: {str(e)}"
        chat_history.append(("assistant", error_msg))
        return error_msg, chat_history
