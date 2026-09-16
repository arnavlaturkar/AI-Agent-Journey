import os
import json
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

def analyze_borrower(borrower_details):
    cot_prompt = """
    You are Jarvis, an AI credit risk analyst.
    Always think step by step:
    Step 1 → Calculate monthly income
    Step 2 → Calculate debt to income ratio
    Step 3 → Calculate monthly payment burden
    Step 4 → Identify risk flags
    Step 5 → Final recommendation
    Show all calculations. Never skip steps.
    """
    return ask(cot_prompt, borrower_details)

borrower1 = "Earns 80,000/year, existing debt 10,000, wants 300/month repayment"
borrower2 = "Earns 30,000/year, existing debt 25,000, wants 800/month repayment"

print("\n=== BORROWER 1 ===")
print(analyze_borrower(borrower1))

print("\n=== BORROWER 2 ===")
print(analyze_borrower(borrower2))