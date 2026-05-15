from app.tools.rag_tool import rag_search
from app.tools.calculator_tool import calculate


TOOLS = {
    "rag_search": rag_search,
    "calculate": calculate
}