def build_prompt(question, scratchpad):

    return f"""
You are an AI agent.

Available tools:

rag_search(query) → search documents
calculate(expression) → perform math

Use this format:

Thought: reasoning
Action: tool_name
Action Input: input
Observation: result

When finished:

Final Answer: answer

Question: {question}

{scratchpad}
"""