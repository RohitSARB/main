import os
import time
import requests

CEREBRAS_BASE = "https://api.cerebras.ai/v1"
CEREBRAS_API_KEY = "csk-ne2dje933kdehkvtdcdveve6vrmvmx48jwed6h4wt5fvtxmd"


def ask_llm(prompt):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CEREBRAS_API_KEY}"
    }

    payload = {
        "model": "llama3.1-8b",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "top_p": 1
    }

    retries = 3

    for attempt in range(retries):

        try:

            res = requests.post(
                f"{CEREBRAS_BASE}/chat/completions",
                headers=headers,
                json=payload,
                timeout=120   # increase timeout
            )

            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"]

            print("Cerebras error:", res.text)

        except requests.exceptions.ReadTimeout:
            print("Timeout — retrying...")

        time.sleep(3)

    raise Exception("LLM request failed after retries")