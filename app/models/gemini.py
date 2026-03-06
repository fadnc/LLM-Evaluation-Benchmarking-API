import time
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def gemini_generate(prompt: str):
    start = time.time()

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    latency = (time.time() - start) * 1000

    return response.text, latency