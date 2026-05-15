from datetime import datetime, timezone
from app.llm.client import generate_response
from app.llm.tokenizer_utils import count_tokens
from app.db.mongo import collection

def run_prompt(prompt, model, temperature, top_p):
    response = generate_response(prompt, model, temperature, top_p)

    if "error" in response:
        return response

    output_text = response["choices"][0]["message"]["content"]

    usage = response.get("usage", {})
    input_tokens = usage.get("prompt_tokens", 0)
    output_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)

    experiment = {
        "prompt": prompt,
        "model": model,
        "temperature": temperature,
        "top_p": top_p,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "response": output_text,
    }

    result = collection.insert_one(experiment)
    
    experiment["_id"] = str(result.inserted_id)
    
    return experiment
