from tools.calculator import calculator


class ToolRegistry:

    def __init__(self, rag):

        self.rag = rag

        self.tools = {
            "calculator": self.calculator,
            "rag_search": self.rag_search
        }

    def calculator(self, query):
        return self.calculator(query)

    def rag_search(self, query):
        return self.rag.ask(query)

    def execute(self, tool_name, tool_input):

        if tool_name not in self.tools:
            return "Unknown tool"

        return self.tools[tool_name](tool_input)