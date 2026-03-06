import os, time
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def groq_generate(prompt: str):
    start = time.time()
    response = client.generate(
        model="llama3-8b-8192",
        messages=[{"role": "user",
                   "content": prompt}]   
    )
    latency = (time.time() - start) * 1000
    return response.choices[0].message.content, latency