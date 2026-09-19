import streamlit as st
import pandas as pd
import json
import time
from credit_agent import analyze_borrower, load_decisions

st.set_page_config(page_title="Credit Risk Agent", page_icon="🏦")

st.title("🏦 AI Credit Risk Agent")
st.markdown("Powered by Groq LLM — enter borrower details or upload a CSV for batch analysis.")

st.divider()

tab1, tab2 = st.tabs(["Single Analysis", "Batch Analysis"])

# ─── TAB 1: Single Analysis ───
with tab1:
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


# ─── TAB 2: Batch Analysis ───
with tab2:
    st.markdown("Upload a CSV file with columns: `name`, `monthly_income`, `monthly_debt`, `repayment_history`")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.subheader("Preview")
        st.table(df)

        required_cols = {"name", "monthly_income", "monthly_debt", "repayment_history"}
        if not required_cols.issubset(df.columns):
            st.error(f"CSV must contain columns: {required_cols}")
        else:
            if st.button("Run Batch Analysis"):
                results = []
                progress = st.progress(0)
                status_text = st.empty()

                for i, row in df.iterrows():
                    status_text.text(f"Analyzing {row['name']} ({i+1}/{len(df)})...")
                    try:
                        result = analyze_borrower(
                            row["name"],
                            row["monthly_income"],
                            row["monthly_debt"],
                            row["repayment_history"]
                        )
                        results.append({
                            "Name": result.get("borrower_name"),
                            "Income": f"${result.get('monthly_income'):,}",
                            "Debt": f"${result.get('monthly_debt'):,}",
                            "DTI %": f"{result.get('dti_ratio'):.1f}%",
                            "Repayment": result.get("repayment_history"),
                            "Risk": result.get("risk_level"),
                            "Decision": result.get("decision"),
                            "Reason": result.get("reason")
                        })
                    except Exception as e:
                        results.append({
                            "Name": row["name"],
                            "Income": row["monthly_income"],
                            "Debt": row["monthly_debt"],
                            "DTI %": "-",
                            "Repayment": row["repayment_history"],
                            "Risk": "ERROR",
                            "Decision": "ERROR",
                            "Reason": str(e)
                        })

                    progress.progress((i + 1) / len(df))
                    time.sleep(0.5)

                status_text.text("✅ Batch analysis complete.")

                results_df = pd.DataFrame(results)

                st.divider()
                st.subheader("📊 Results")

                approve_count = len(results_df[results_df["Decision"] == "APPROVE"])
                reject_count = len(results_df[results_df["Decision"] == "REJECT"])
                total = len(results_df)

                col1, col2, col3 = st.columns(3)
                col1.metric("Total Borrowers", total)
                col2.metric("Approved ✅", approve_count)
                col3.metric("Rejected ❌", reject_count)

                st.table(results_df)

                csv_out = results_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Download Results CSV",
                    data=csv_out,
                    file_name="batch_results.csv",
                    mime="text/csv"
                )
                