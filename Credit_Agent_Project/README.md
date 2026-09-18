# 🏦 AI Credit Risk Agent

An agentic AI application that evaluates borrower profiles and delivers instant credit risk decisions using a Large Language Model (LLM).

Built as Portfolio Project 1 in my transition from Data Analysis into Agentic AI Engineering.

---

## 🎯 What It Does

- Takes borrower inputs: name, monthly income, monthly debt, repayment history
- Sends structured data to an LLM with a domain-specific system prompt
- LLM calculates DTI ratio, assigns risk level, and returns a JSON decision
- App displays APPROVE ✅ or REJECT ❌ with full reasoning
- Persists all decisions to a local JSON file for audit trail

---

## 🧠 Core Concepts Demonstrated

| Concept | Implementation |
|---|---|
| Prompt Engineering | System prompt with explicit rules, formulas, and output schema |
| Structured Output | LLM returns pure JSON — parsed and acted on by code |
| Chain of Thought | LLM reasons through DTI → risk level → decision sequentially |
| Tool + Memory | Decisions saved and retrieved from `credit_decisions.json` |
| Agent UI | Streamlit front-end for real-time interaction |

---

## 🛠️ Tech Stack

- **LLM:** Groq API
- **UI:** Streamlit
- **Language:** Python 3.11
- **Libraries:** `groq`, `python-dotenv`, `streamlit`

---

## 📁 Project Structure
Credit_Agent_Project/
├── app.py # Streamlit UI
├── credit_agent.py # LLM logic, DTI analysis, decision saving
└── credit_decisions.json # Persistent decision log

---

## ⚙️ Setup & Run

1. Clone the repo and navigate to the project:
```bash
git clone https://github.com/arnavlaturkar/AI-Agent-Journey
cd AI-Agent-Journey/Credit_Agent_Project
```

2. Create and activate conda environment:
```bash
conda create -n agent-env python=3.11
conda activate agent-env
```

3. Install dependencies:
```bash
python -m pip install groq python-dotenv streamlit
```

4. Add your Groq API key to a `.env` file in the root:

5. Run the app:
```bash
streamlit run app.py
```

---

## 📊 Sample Decision Output

```json
{
  "borrower_name": "Jack",
  "monthly_income": 4000,
  "monthly_debt": 1200,
  "dti_ratio": 30.0,
  "repayment_history": "Good",
  "risk_level": "MEDIUM",
  "decision": "APPROVE",
  "reason": "DTI is 30% and repayment history is good, so risk is medium and loan approved."
}
```

---
## 📸 Screenshots

**Input Form**
![Input Form](screenshots/form.png)

**Json Form**
![Data Json Format](screenshots/json_form.png)

**Approve Decision**
![Approve Decision](screenshots/approve.png)

**Reject Decision**
![Reject Decision](screenshots/reject.png)

---

## 👤 Author

**Arnav Laturkar**  
Business Data Analyst → Agentic AI Engineer  
[GitHub](https://github.com/arnavlaturkar/AI-Agent-Journey)