import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation_history = [
    {"role": "system", "content": "You are Jarvis, an AI data analyst agent. You analyze data and give clear concise insights."}
]

print("Jarvis is ready! Type 'quit' to exit\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "quit":
        print("Jarvis shutting down...")
        break
    
    conversation_history.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=conversation_history
    )
    
    reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": reply})
    
    print(f"\nJarvis: {reply}\n")