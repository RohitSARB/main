from services.llm_service import ask_llm


class ReActAgent:

    def __init__(self, tool_registry):

        self.tool_registry = tool_registry

    def run(self, query):

        prompt = f"""
You are an AI agent.

Available tools:
calculator
rag_search

Question: {query}

Respond using:

Thought:
Action:
Action Input:
"""

        for _ in range(5):

            response = ask_llm(prompt)

            print(response)

            if "Final Answer:" in response:
                return response.split("Final Answer:")[-1].strip()

            if "Action:" in response:

                tool = response.split("Action:")[1].split("\n")[0].strip()
                tool_input = response.split("Action Input:")[1].strip()

                observation = self.tool_registry.execute(tool, tool_input)

                prompt += f"\nObservation: {observation}\n"

        return "Agent stopped."