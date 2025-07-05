import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# ==== Configure Gemini API ====
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro")

def ask_assistant(symptoms, weight, height, age):

    prompt = f"""
    Act as a medical assistant. A user has described their symptoms:
    "{symptoms}"
    They are {weight} kg, {height} cm tall, and {age} years old.

    Please:
    1. Suggest whether these symptoms may relate to PCOD.
    2. Rate the urgency (Low, Medium, High).
    3. Recommend if a gynecologist should be consulted.
    4. Offer general advice for care.
    5. Briefly assess if the symptoms might relate to PCOD/PCOS.
    6. Rate the urgency: Low, Medium, or High.
    4. Give short, actionable general advice.

Limit total response to under 300 words. Do not include disclaimers — the app will handle that.

    Do not provide a diagnosis.
    """
    
    response = model.generate_content(prompt)
    advice = response.text

    return advice