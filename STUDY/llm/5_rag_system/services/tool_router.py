from tools.calculator import calculator

class ToolsRouter:
    def route(self, query):
        if any(x in query for x in ["*", "+", "-", "/"]):
            return "calculator"
        return "rag"
    
    def execute(self, tool, query):
        if tool == "calculator":
            return calculator(query)
        
        return None