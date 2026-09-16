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

few_shot_prompt = """
You are Jarvis, a credit risk analyst.
Always analyze borrowers in EXACTLY this format:

EXAMPLE 1:
Borrower: Earns 60,000/year, existing debt 5,000, wants 200/month repayment
RISK LEVEL: LOW
MONTHLY INCOME: $5,000
DTI RATIO: 8.3%
MONTHLY BURDEN: 4% of income
RED FLAGS: None
RECOMMENDATION: APPROVE — Low DTI, manageable payment burden

EXAMPLE 2:
Borrower: Earns 35,000/year, existing debt 30,000, wants 700/month repayment
RISK LEVEL: HIGH
MONTHLY INCOME: $2,917
DTI RATIO: 85.7%
MONTHLY BURDEN: 24% of income
RED FLAGS: DTI exceeds 43%, existing debt close to annual income
RECOMMENDATION: REJECT — DTI too high, borrower overleveraged

Now analyze the next borrower in EXACTLY the same format.
"""
borrowers = [
    "Earns 90,000/year, existing debt 8,000, wants 250/month repayment",
    "Earns 25,000/year, existing debt 20,000, wants 600/month repayment",
    "Earns 55,000/year, existing debt 12,000, wants 350/month repayment"
]

print("\n=== BATCH ANALYSIS ===")
for i, borrower in enumerate(borrowers, 1):
    print(f"\n--- Borrower {i} ---")
    print(ask(few_shot_prompt, borrower))