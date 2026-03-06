import time
import os
import anthropic

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def claude_generate(prompt: str):
    start = time.time()

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    latency = (time.time() - start) * 1000

    text = response.content[0].text

    return text, latency