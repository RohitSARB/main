from openai import OpenAI
from app.config import settings


class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_answer(self, question: str, context: str) -> str:
        prompt = f"""
You are an enterprise technical assistant.

Use ONLY the context below to answer the question.

Context:
{context}

Question:
{question}

If the answer is not in context, say:
"I could not find this information in the knowledge base."
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful enterprise assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content
