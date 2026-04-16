import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def improve_bullet(prompt):

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)

    # google-generativeai responses expose text via `response.text`, not `choices`.
    if getattr(response, "text", None):
        return response.text

    # Fallback for cases where text is not directly populated.
    candidates = getattr(response, "candidates", None) or []
    if candidates:
        parts = getattr(candidates[0].content, "parts", None) or []
        if parts and getattr(parts[0], "text", None):
            return parts[0].text

    raise ValueError("Gemini returned an empty response. Please try again.")
