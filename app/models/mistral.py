import os
import time
from mistralai.client import MistralClient

API_KEY = os.getenv("MISTRAL_API_KEY")

client = None
if API_KEY:
    client = MistralClient(api_key=API_KEY)


def mistral_generate(prompt: str):
    if client is None:
        raise ValueError("Mistral API key not configured")

    start = time.time()

    response = client.chat(
        model="mistral-small",
        messages=[{"role": "user", "content": prompt}]
    )

    latency = (time.time() - start) * 1000
    text = response.choices[0].message.content

    return text, latency