import json

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.memory = []

    def think(self, task):
        self.memory.append(task)
        print(f"{self.name} is thinking about: {task}")

    def show_memory(self):
        print(f"\n{self.name}'s memory:")
        for m in self.memory:
            print(f"  - {m}")
    
    def save_memory(self):
        with open(f"{self.name}_memory.json", "w") as f:
         json.dump(self.memory, f)
         print(f"{self.name}'s memory saved!")
    
    def load_memory(self):
     try:
        with open(f"{self.name}_memory.json", "r") as f:
            self.memory = json.load(f)
            print(f"{self.name}'s memory loaded!")
     except FileNotFoundError:
        print(f"No memory found for {self.name}")
    
my_agent = Agent("Jarvis", "Research")
my_agent.load_memory()
my_agent.show_memory()

