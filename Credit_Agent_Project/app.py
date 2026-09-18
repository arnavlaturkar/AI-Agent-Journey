import streamlit as st
import json
from credit_agent import analyze_borrower, load_decisions

st.set_page_config(page_title="Credit Risk Agent", page_icon="🏦")

st.title("🏦 AI Credit Risk Agent")
st.markdown("Powered by Groq LLM — enter borrower details to get an instant risk decision.")

st.divider()

with st.form("borrower_form"):
    name = st.text_input("Borrower Name")
    income = st.number_input("Monthly Income ($)", min_value=0, step=100)
    debt = st.number_input("Monthly Debt ($)", min_value=0, step=100)
    repayment = st.selectbox(
        "Repayment History",
        ["Excellent", "Good", "Fair", "Poor"]
    )
    submitted = st.form_submit_button("Analyze Risk")

if submitted:
    if not name or income == 0:
        st.warning("Please enter borrower name and income.")
    else:
        with st.spinner("Analyzing borrower..."):
            try:
                result = analyze_borrower(name, income, debt, repayment)

                st.divider()

                decision = result.get("decision")
                risk = result.get("risk_level")

                if decision == "APPROVE":
                    st.success(f"✅ APPROVED — {risk} RISK")
                else:
                    st.error(f"❌ REJECTED — {risk} RISK")

                col1, col2, col3 = st.columns(3)
                col1.metric("Monthly Income", f"${result.get('monthly_income'):,}")
                col2.metric("Monthly Debt", f"${result.get('monthly_debt'):,}")
                col3.metric("DTI Ratio", f"{result.get('dti_ratio'):.1f}%")

                st.info(f"📝 {result.get('reason')}")

                with st.expander("Full JSON Response"):
                    st.json(result)

            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.subheader("📂 Past Decisions")

decisions = load_decisions()
if decisions:
    for d in reversed(decisions):
        status = "✅" if d.get("decision") == "APPROVE" else "❌"
        st.markdown(f"{status} **{d.get('borrower_name')}** — {d.get('risk_level')} risk — DTI: {d.get('dti_ratio'):.1f}%")
else:
    st.caption("No decisions yet.")