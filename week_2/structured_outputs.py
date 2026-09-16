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

json_prompt = """
You are Jarvis, a credit risk analyst.
Always respond in pure JSON format only.
No extra text, no markdown, no explanation.

Use EXACTLY these formulas step by step:
- monthly_income = annual_income / 12
- existing_debt_payment = existing_debt / 24  (assume 2 year repayment)
- total_monthly_debt = existing_debt_payment + new_monthly_repayment
- dti_ratio = (total_monthly_debt / monthly_income) * 100

Risk rules:
- dti_ratio below 30 = LOW risk → APPROVE
- dti_ratio 30-43 = MEDIUM risk → APPROVE with conditions
- dti_ratio above 43 = HIGH risk → REJECT

Return exactly this structure:
{
    "risk_level": "LOW/MEDIUM/HIGH",
    "monthly_income": number,
    "existing_debt_payment": number,
    "total_monthly_debt": number,
    "dti_ratio": number,
    "red_flags": ["list of red flags or empty list"],
    "recommendation": "APPROVE/REJECT",
    "reason": "one line explanation"
}
"""

def analyze_borrower(borrower_details):
    result = ask(json_prompt, borrower_details)
    parsed = json.loads(result)
    return parsed

def make_decision(borrower_details):
    result = analyze_borrower(borrower_details)
    
    print(f"\nAnalyzing: {borrower_details}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"DTI Ratio: {result['dti_ratio']}")
    print(f"Recommendation: {result['recommendation']}")
    
    if result['recommendation'] == "APPROVE":
        print("✅ AUTO APPROVED — Sending approval notification")
    elif result['recommendation'] == "REJECT":
        print("❌ AUTO REJECTED — Flagged for review")

borrowers = [
    "Earns 90,000/year, existing debt 8,000, wants 250/month repayment",
    "Earns 25,000/year, existing debt 20,000, wants 600/month repayment",
    "Earns 55,000/year, existing debt 12,000, wants 350/month repayment"
]

for borrower in borrowers:
    make_decision(borrower)