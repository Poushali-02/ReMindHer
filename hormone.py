# logic for hormone tracker using gemini
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

def ask_about_hormones(age, gender, weight, height, Menstrual_history, symptoms, lifestyle_factors, medical_history):

    prompt = f"""
Act as a medical assistant. A user has described their symptoms and background health data.

Age: {age} years  
Gender: {gender}  
Weight: {weight} kg  
Height: {height} cm  

Menstrual History: {Menstrual_history}  
Symptoms: {symptoms}  
Lifestyle Factors: {lifestyle_factors}  
Medical History: {medical_history}  

Please:
1. Suggest which hormones might be imbalanced based on the symptoms.
2. Suggest whether these symptoms relate to PCOD/PCOS or other hormone issues.
3. Rate the urgency (Low, Medium, High).
4. Recommend if a gynecologist or specialist should be consulted.
5. Offer general advice for care.
6. Briefly explain if the user's lifestyle or medical history might be contributing to this.
7. Provide short, actionable advice.

Limit the response to under 300 words. Do not include disclaimers – the app will handle that.
"""

    
    response = model.generate_content(prompt)
    advice = response.text

    return advice