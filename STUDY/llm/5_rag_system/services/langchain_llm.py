# from langchain_core.runnables import Runnable
# from services.llm_service import ask_llm


# class CerebrasRunnable(Runnable):

#     def invoke(self, input, config=None):

#         if isinstance(input, dict):
#             prompt = str(input)
#         else:
#             prompt = input

#         response = ask_llm(prompt)

#         return response



from langchain_core.runnables import Runnable
from langchain_core.messages import BaseMessage
from langchain_core.messages import AIMessage
from services.llm_service import ask_llm


class CerebrasRunnable(Runnable):

    def invoke(self, input, config=None):

        # Case 1: ChatPromptValue (most common)
        if hasattr(input, "to_messages"):
            messages = input.to_messages()
            # prompt = "\n".join([msg.content for msg in messages])
            prompt = "\n".join([f"{msg.type}: {msg.content}" for msg in messages])

        # Case 2: Already messages
        # elif isinstance(input, list) and isinstance(input[0], BaseMessage):
        elif isinstance(input, list) and len(input) > 0 and isinstance(input[0], BaseMessage):
            prompt = "\n".join([msg.content for msg in input])

        # Case 3: dict
        # elif isinstance(input, dict):
        #     prompt = str(input)
        elif isinstance(input, dict):
            prompt = "\n".join(f"{k}: {v}" for k, v in input.items())

        # Case 4: plain string
        else:
            prompt = str(input)
        
        print("Prompt sent to LLM:\n", prompt)
        
        # return ask_llm(prompt)
        return AIMessage(content=ask_llm(prompt))