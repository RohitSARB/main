import os, requests

CEREBRAS_BASE = "https://api.cerebras.ai/v1"
# CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
CEREBRAS_API_KEY = 'csk-ne2dje933kdehkvtdcdveve6vrmvmx48jwed6h4wt5fvtxmd'

def generate_response(prompt, model, temperature, top_p):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CEREBRAS_API_KEY}"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "top_p": top_p
    }

    try:
        res = requests.post(
            f"{CEREBRAS_BASE}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        data = res.json()
        if res.status_code != 200:
            return {"error": data}
        return data
    except Exception as e:
        return {"error": str(e)}
