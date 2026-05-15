# from services.memory_service import MemoryService
# from services.tool_router import ToolsRouter
# from services.rag_pipeline import RAGPipeline
# from services.llm_service import ask_llm

# class Assistant:
#     def __init__(self, documents):
#         self.memory = MemoryService()
#         self.router = ToolsRouter()
#         self.rag = RAGPipeline(documents)
    
#     def chat(self, user_input):
#         self.memory.add("user", user_input)
#         tool = self.router.route(user_input)
#         if tool == "calculator":
#             result = self.router.execute(tool, user_input)
#             response = f'Result: {result}'
        
#         else:
#             response = self.rag.ask(user_input)
        
#         self.memory.add("assistant", response)
#         return response



from services.react_agent import ReActAgent
from services.tool_registry import ToolRegistry
from services.rag_pipeline import RAGPipeline


class Assistant:

    def __init__(self, documents):

        self.rag = RAGPipeline(documents)
        registry = ToolRegistry(self.rag)
        self.agent = ReActAgent(registry)

    def chat(self, query):

        return self.agent.run(query)