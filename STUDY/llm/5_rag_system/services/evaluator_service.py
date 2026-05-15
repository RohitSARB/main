from services.llm_service import ask_llm


class EvaluatorService:

    def evaluate(self, question, expected, answer):

        prompt = f"""
You are an AI evaluator.

Question:
{question}

Expected Answer:
{expected}

Model Answer:
{answer}

Give a score from 1-10 based on correctness.

Return format:

Score: <number>
Reason: <short explanation>
"""

        result = ask_llm(prompt)

        return result