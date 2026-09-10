import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(system_prompt, user_message):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content

weak_prompt = "You are a helpful assistant."

strong_prompt = """
You are Jarvis, an expert AI data analyst specializing in financial data,credit risk and consulting. 
You:
- Always give structured, concise answers
- Use bullet points for clarity
- Ask clarifying questions when data is ambiguous
- Never make assumptions without stating them
- Always mention data limitations
- Provide actionable insights and recommendations based on data analysis
- Always consider the context of the data and the business implications of your analysis
"""

question = "What should I look at when analyzing a loan portfolio?"

print("=== WEAK PROMPT ===")
print(ask(weak_prompt, question))

print("\n=== STRONG PROMPT ===")
print(ask(strong_prompt, question))

analyst_prompt = "You are a senior credit risk analyst at a bank with 15 years experience."
startup_prompt = "You are an AI startup founder building a fintech lending product."

question = "What is the biggest risk in lending right now?"

print("=== CREDIT RISK ANALYST ===")
print(ask(analyst_prompt, question))

print("\n=== STARTUP FOUNDER ===")
print(ask(startup_prompt, question))