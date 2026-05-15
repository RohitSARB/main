from services.llm_service import ask_llm
from app.tools.rag_tool import rag_search
from app.tools.calculator_tool import calculate


TOOLS = {
    "rag_search": rag_search,
    "calculate": calculate
}


class SimpleAgent:

    def run(self, question):

        prompt = f"""
You are an AI agent.

You have access to tools:

rag_search(query)
calculate(expression)

Use this format:

Thought: reasoning
Action: tool_name
Action Input: input
Observation: result

When finished:

Final Answer: answer

Question: {question}
"""

        for _ in range(3):

            response = ask_llm(prompt)

            print(response)

            if "Final Answer:" in response:
                return response

            # extract tool
            lines = response.split("\n")

            action = None
            action_input = None

            for line in lines:

                if line.startswith("Action:"):
                    action = line.split(":")[1].strip()

                if line.startswith("Action Input:"):
                    action_input = line.split(":")[1].strip()

            if action in TOOLS:

                result = TOOLS[action](action_input)

                prompt += f"\nObservation: {result}\n"

        return "Agent stopped"
    

agent = SimpleAgent()

question = "What is FAISS?"

agent.run(question)