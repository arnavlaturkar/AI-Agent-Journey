import requests
import json

def get_weather(city):
    try:
        response = requests.get(f"https://wttr.in/{city}?format=j1")
        data = response.json()
        temperature = data["current_condition"][0]["temp_C"]
        weather = data["current_condition"][0]["weatherDesc"][0]["value"]
        return f"{city}: {temperature}°C, {weather}"
    except:
        return f"Could not get weather for {city}"

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.memory = []

    def think(self, task):
        self.memory.append(task)
        print(f"{self.name} is thinking about: {task}")

    def use_tool(self, tool, input):
        result = tool(input)
        self.memory.append(f"used tool → {result}")
        print(f"{self.name} got result: {result}")

    def show_memory(self):
        print(f"\n{self.name}'s memory:")
        for m in self.memory:
            print(f"  - {m}")

my_agent = Agent("Jarvis", "Research")
my_agent.think("check weather for user")
city = input("Which city do you want weather for? ")
my_agent.use_tool(get_weather, city)
my_agent.show_memory()
