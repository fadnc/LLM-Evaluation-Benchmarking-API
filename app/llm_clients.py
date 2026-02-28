import os
import time
import requests
import google.generativeai as genai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def call_openai(prompt: str):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    start = time.perf_counter()
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    latency = (time.perf_counter() - start) * 1000

    content = response.json()["choices"][0]["message"]["content"]
    return content, latency


def call_gemini(prompt: str):
    start = time.perf_counter()

    model = genai.GenerativeModel("gemini-1.0-pro")
    response = model.generate_content(prompt)

    latency = (time.perf_counter() - start) * 1000

    return response.text, latency


def call_mock(prompt: str):
    start = time.perf_counter()
    response = f"Mock response for: {prompt}"
    latency = (time.perf_counter() - start) * 1000
    return response, latency