import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def improve_bullet(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a resume optimization expert."},
            {"role": "user", "content": prompt}
        ],
        temperature = 0.7
    )
    return response.choices[0].message.content
