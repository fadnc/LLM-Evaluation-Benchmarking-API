import time
import random

def mock_generate(prompt: str):
    start = time.time()

    time.sleep(0.01)

    response = f"Mock response to: {prompt}"

    latency = (time.time() - start) * 1000

    return response, latency