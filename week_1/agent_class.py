class Agent():                 
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.memory = []

    def think(self, task):
        self.memory.append(task)
        print(f"{self.name} is thinking about {task}")
        
    def show_memory(self):
        print(f"\n{self.name}'s memory:")
        for m in self.memory:
            print(f"- {m}")
            
class ResearchAgent(Agent):
    def search(self,query):
        print(f"{self.name} is searching {query}")
        self.memory.append(f"searched for {query}")
        

my_agent_1 = Agent("Jarvis", "Research")
my_agent_2 = Agent("Ultron", "Analysis")

my_agent_1.think(": find the Tesla stock data")
my_agent_1.think(": analyze the last 5 years data")
my_agent_2.think(": compare with Apple stocks")
my_agent_2.think(": generate a report")

my_agent_1.show_memory()
my_agent_2.show_memory()

researcher = ResearchAgent("Jarvis", "Research")
researcher.think(": what should I search ?")
researcher.search(": Teslas Q4 earnings 2026 ")
researcher.show_memory()