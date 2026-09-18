import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
DECISIONS_FILE = "Credit_Agent_Project/credit_decisions.json"

def load_decisions():
    if os.path.exists(DECISIONS_FILE):
        with open(DECISIONS_FILE, "r") as f:
            return json.load(f)
    return []

def save_decision(decision):
    decisions = load_decisions()
    decisions.append(decision)
    with open(DECISIONS_FILE, "w") as f:
        json.dump(decisions, f, indent=2)

def analyze_borrower(name, income, debt, repayment_history):
    system_prompt = """You are a credit risk analyst. Analyze borrower data and return ONLY a JSON object.

Rules:
- DTI = (monthly_debt / monthly_income) * 100. Calculate this exactly.
- Risk levels: LOW (DTI < 30), MEDIUM (DTI 30-50), HIGH (DTI > 50)
- Repayment history weight: excellent=+1 tier safer, poor=+1 tier riskier
- Decision: APPROVE if final risk is LOW or MEDIUM, REJECT if HIGH

Return this exact structure, nothing else:
{
  "borrower_name": "string",
  "monthly_income": number,
  "monthly_debt": number,
  "dti_ratio": number,
  "repayment_history": "string",
  "risk_level": "LOW | MEDIUM | HIGH",
  "decision": "APPROVE | REJECT",
  "reason": "one sentence explanation"
}"""

    user_message = f"""
Borrower: {name}
Monthly Income: ${income}
Monthly Debt: ${debt}
Repayment History: {repayment_history}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.1
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown code blocks if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    result = json.loads(raw)
    save_decision(result)
    return result