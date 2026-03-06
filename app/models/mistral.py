import os
import time
from mistralai import Mistral

API_KEY = os.getenv("MISTRAL_API_KEY")

client = Mistral(api_key=API_KEY) if API_KEY else None

def mistral_generate(prompt: str):
    if client is None:
        raise ValueError("Mistral API key not configured")

    start = time.time()

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}]
    )

    latency = (time.time() - start) * 1000
    text = response.choices[0].message.content

    return text, latency