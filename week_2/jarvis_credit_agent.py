import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

system_prompt = """
You are Jarvis, an expert AI credit risk analyst with 15 years experience.

Always analyze borrowers step by step:
Step 1 → Calculate monthly income (annual / 12)
Step 2 → Calculate existing debt payment (existing debt / 24)
Step 3 → Calculate total monthly debt (existing payment + new repayment)
Step 4 → Calculate DTI ratio (total monthly debt / monthly income * 100)
Step 5 → Identify red flags
Step 6 → Make final decision

Risk rules:
- DTI below 30 = LOW risk → APPROVE
- DTI 30-43 = MEDIUM risk → APPROVE with conditions
- DTI above 43 = HIGH risk → REJECT

Always respond in pure JSON only. No extra text. No markdown.

Return exactly this structure:
{
    "borrower_summary": "one line description",
    "monthly_income": number,
    "existing_debt_payment": number,
    "total_monthly_debt": number,
    "dti_ratio": number,
    "risk_level": "LOW/MEDIUM/HIGH",
    "red_flags": ["list or empty"],
    "recommendation": "APPROVE/REJECT",
    "reason": "one line explanation"
}
"""

def analyze_borrower(name, annual_income, existing_debt, monthly_repayment):
    borrower_details = f"""
    Borrower name: {name}
    Annual income: ${annual_income}
    Existing debt: ${existing_debt}
    Requested monthly repayment: ${monthly_repayment}
    """
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": borrower_details}
        ]
    )
    
    result = response.choices[0].message.content
    parsed = json.loads(result)
    parsed["name"] = name
    return parsed
def save_decisions(decisions):
    with open("credit_decisions.json", "w") as f:
        json.dump(decisions, f, indent=4)
    print(f"\n✅ {len(decisions)} decisions saved to credit_decisions.json")

def print_result(result):
    print(f"\n{'='*40}")
    print(f"Borrower: {result['name']}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Monthly Income: ${result['monthly_income']}")
    print(f"DTI Ratio: {result['dti_ratio']}%")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Reason: {result['reason']}")
    if result['red_flags']:
        print(f"Red Flags: {result['red_flags']}")
    if result['recommendation'] == "APPROVE":
        print("✅ AUTO APPROVED")
    else:
        print("❌ AUTO REJECTED")
        
borrowers = [
    {"name": "John Smith", "annual_income": 90000, "existing_debt": 8000, "monthly_repayment": 250},
    {"name": "Raj Patel", "annual_income": 25000, "existing_debt": 20000, "monthly_repayment": 600},
    {"name": "Sarah Jones", "annual_income": 55000, "existing_debt": 12000, "monthly_repayment": 350},
    {"name": "Priya Shah", "annual_income": 120000, "existing_debt": 5000, "monthly_repayment": 400},
]

print("🤖 Jarvis Credit Risk Agent Starting...\n")

decisions = []

for borrower in borrowers:
    result = analyze_borrower(
        borrower["name"],
        borrower["annual_income"],
        borrower["existing_debt"],
        borrower["monthly_repayment"]
    )
    print_result(result)
    decisions.append(result)

save_decisions(decisions)

approved = [d for d in decisions if d["recommendation"] == "APPROVE"]
rejected = [d for d in decisions if d["recommendation"] == "REJECT"]

print(f"\n📊 FINAL SUMMARY")
print(f"Total Analyzed: {len(decisions)}")
print(f"Approved: {len(approved)}")
print(f"Rejected: {len(rejected)}")