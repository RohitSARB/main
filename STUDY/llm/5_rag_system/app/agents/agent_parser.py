class AgentParser:

    def parse(self, text):

        if "Final Answer:" in text:
            answer = text.split("Final Answer:")[-1].strip()
            return {"type": "finish", "answer": answer}

        action = None
        action_input = None

        for line in text.split("\n"):

            if line.startswith("Action:"):
                action = line.split(":")[1].strip()

            if line.startswith("Action Input:"):
                action_input = line.split(":")[1].strip()

        if action:
            return {
                "type": "action",
                "tool": action,
                "input": action_input
            }

        return {"type": "unknown"}