import time
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def openai_generate(prompt: str):
    start = time.time()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    latency = (time.time() - start) * 1000

    text = response.choices[0].message.content

    return text, latency