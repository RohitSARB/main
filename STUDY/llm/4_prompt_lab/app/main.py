from fastapi import FastAPI
from pydantic import BaseModel
from app.services.prompt_service import run_prompt

app = FastAPI()

'''
VARIOUS MODELS:
llama-3.3-70b
qwen-3-32b
zai-glm-4.7
gpt-oss-120b
'''

'''
FOR CEREBRAS:
- llama3.1-8b
- qwen-3-32b
- gpt-oss-120b
'''

class PromptRequest(BaseModel):
    prompt: str
    # model: str = "gpt-3.5-turbo"
    model: str = "llama3.1-8b"
    temperature: float = 0.6
    top_p: float = 1.0

@app.post("/run")
def run(request: PromptRequest):
    return run_prompt(
        request.prompt,
        request.model,
        request.temperature,
        request.top_p
    )
