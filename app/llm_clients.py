import requests
import os
import time

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def call_gemini(prompt: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7
        }
    }

    start = time.perf_counter()
    response = requests.post(url, headers=headers, json=payload)
    latency = (time.perf_counter() - start) * 1000

    result = response.json()
    content = result["candidates"][0]["content"]["parts"][0]["text"]

    return content, latency


def call_mock(prompt: str):
    start = time.perf_counter()
    response = f"Mock response for: {prompt}"
    latency = (time.perf_counter() - start) * 1000
    return response, latency