import time
import os
import anthropic

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def claude_generate(prompt: str):
    start = time.time()

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    latency = (time.time() - start) * 1000

    text = response.content[0].text

    return text, latency