import time
import requests

def ollama_generate(prompt: str):
    start = time.time()

    response = requests.post(
        "http://host.docker.internal:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    latency = (time.time() - start) * 1000

    text = response.json()["response"]

    return text, latency