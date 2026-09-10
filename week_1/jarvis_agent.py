import os   #reads environment variables from your system. Used to get your API key securely.
import json
import requests #get_weather() to call the weather API.
from dotenv import load_dotenv # reads .env file.
from groq import Groq

load_dotenv()   #reads the .env file and loads GROQ_API_KEY into your environment.

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_weather(city):    # weather tool
    try:
        response = requests.get(f"https://wttr.in/{city}?format=j1")
        data = response.json()
        temperature = data["current_condition"][0]["temp_C"]
        weather = data["current_condition"][0]["weatherDesc"][0]["value"]
        return f"{city}: {temperature}°C, {weather}"
    except:
        return f"Could not get weather for {city}"
    
class Agent:   #agent class
     def __init__(self, name, role):
        self.name = name
        self.role = role
        self.memory = []
        self.conversation_history = [
            {"role": "system", "content": f"You are {name}, an AI {role} agent. You analyze data and give clear concise insights."}
        ]

     def think(self, task): # think function
        self.memory.append(task)
        print(f"{self.name} is thinking about: {task}")

     def save_memory(self): #save memory to json file 
        with open(f"{self.name}_memory.json", "w") as f:
            json.dump(self.memory, f)
        print(f"{self.name}'s memory saved!")

     def load_memory(self): #load memory from json file if available 
        try:
            with open(f"{self.name}_memory.json", "r") as f:
                self.memory = json.load(f)
            print(f"{self.name}'s memory loaded!")
        except FileNotFoundError:
            print(f"No memory found for {self.name}")

     def chat(self, user_input):    # ← same indentation as other methods
        self.conversation_history.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=self.conversation_history
        )
        
        reply = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": reply})
        self.memory.append(f"User asked: {user_input}")
        
        return reply
            
     
jarvis = Agent("Jarvis", "data analyst") # Run agent
jarvis.load_memory()

print(f"\n{jarvis.name} is ready! Type 'weather' for weather, 'memory' to see memory, 'quit' to exit\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "quit":
        jarvis.save_memory()
        print("Jarvis shutting down...")
        break
    
    elif user_input.lower() == "weather":
        city = input("Which city? ")
        result = get_weather(city)
        print(f"\nJarvis: {result}\n")
    
    elif user_input.lower() == "memory":
        print(f"\nJarvis's memory:")
        for m in jarvis.memory:
            print(f"  - {m}")
        print()
    
    else:
        reply = jarvis.chat(user_input)
        print(f"\nJarvis: {reply}\n") 