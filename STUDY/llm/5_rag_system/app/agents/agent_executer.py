from services.llm_service import ask_llm
from app.agents.agent_prompt import build_prompt
from app.agents.agent_parser import AgentParser
from app.tools.tool_registry import TOOLS


class AgentExecutor:

    def __init__(self):

        self.parser = AgentParser()

    def run(self, question):

        scratchpad = ""

        for step in range(5):

            prompt = build_prompt(question, scratchpad)

            response = ask_llm(prompt)

            print(response)

            parsed = self.parser.parse(response)

            if parsed["type"] == "finish":
                return parsed["answer"]

            if parsed["type"] == "action":

                tool = parsed["tool"]
                tool_input = parsed["input"]

                if tool in TOOLS:

                    result = TOOLS[tool](tool_input)

                    scratchpad += f"""
{response}
Observation: {result}
"""

                else:

                    scratchpad += f"""
{response}
Observation: Tool not found
"""
                    


if __name__ == "__main__":
    agent = AgentExecutor()

    question = "What is FAISS?"

    answer = agent.run(question)

    print("\nFINAL ANSWER:", answer)