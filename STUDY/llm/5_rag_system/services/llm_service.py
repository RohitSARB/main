import time
import requests


CEREBRAS_BASE = "https://api.cerebras.ai/v1"
CEREBRAS_API_KEY = 'csk-ne2dje933kdehkvtdcdveve6vrmvmx48jwed6h4wt5fvtxmd'


def ask_llm(prompt):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CEREBRAS_API_KEY}"
    }

    payload = {
        "model": "llama3.1-8b",
        "messages": [
            {"role": "system", "content": "You answer using provided context."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    for _ in range(3):

        try:

            res = requests.post(
                f"{CEREBRAS_BASE}/chat/completions",
                headers=headers,
                json=payload,
                timeout=120
            )

            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"]

        except requests.exceptions.ReadTimeout:
            print("Retrying...")

        time.sleep(3)

    raise Exception("LLM failed")