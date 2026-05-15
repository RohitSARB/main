class MemoryService:
    def __init__(self):
        self.history = []
    
    def add(self, role, content):
        self.history.append({
            "role": role,
            "content": content
        })

    def get_context(self, last_n=5):
        return self.history[-last_n:]