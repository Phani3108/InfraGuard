import streamlit as st
import json
_PROVENANCE = bytes([80,104,97,110,105,32,77,97,114,117,112,97,107,97]).decode()  # noqa: F841
from iam_policy_analyzer.analyzer import analyze_policy, generate_least_privilege, explain_risk
from kafka_lag_explainer.lag_analyzer import analyze_kafka_lag
import pandas as pd
from infra_change_summarizer.summarizer import summarize_terraform_diff
from decision_engine.engine import assess_risk
from action_generator.generator import generate_action_summary



# Streamlit UI setup
st.set_page_config(page_title="InfraGuard AI", layout="wide")

st.title("🛡️ InfraGuard AI — DevOps Risk Assistant")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "IAM Policy Analyzer",
    "Kafka Lag Explainer",
    "Terraform Risk Summarizer",
    "Decision Engine",
    "Notifications" 
])


from datetime import datetime


def render_chat_message(title, summary):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.markdown(f"""
    <div style="
        background-color: #1f2937;
        color: #f9fafb;
        padding: 16px;
        border-radius: 10px;
        margin-bottom: 16px;
        font-family: 'Segoe UI', sans-serif;
        line-height: 1.6;
        word-wrap: break-word;
        overflow-wrap: break-word;
        white-space: pre-wrap;
        max-width: 100%;
    ">
        <div style="font-size: 14px; color: #9ca3af;">
            🤖 InfraGuard Bot &nbsp;|&nbsp; {now}
        </div>
        <div style="margin-top: 10px; font-size: 16px;">
            <b>{title}</b>
        </div>
        <div style="margin-top: 12px; font-size: 15px;">
            {summary}
    """, unsafe_allow_html=True)




# --- TAB 1: IAM Policy Analyzer ---
with tab1:
    st.header("🔐 IAM Policy Analyzer")

    uploaded_policy = st.file_uploader("Upload IAM policy JSON", type=["json"])

    if uploaded_policy:
        try:
            policy = json.load(uploaded_policy)
            st.subheader("📄 Uploaded IAM Policy")
            st.json(policy)

            # Over-permissiveness detection
            st.subheader("🛡️ Detected Issues")
            findings = analyze_policy(policy)
            if findings:
                for issue in findings:
                    st.json(issue)

                # AI Explanation
                st.subheader("🔎 AI Explanation of Risk")
                explanation = explain_risk(policy)
                st.markdown(explanation)
            else:
                st.success("✅ No over-permissive access found.")

            # AI Least-privilege rewrite
            st.subheader("🔁 Least-Privilege Rewrite (via Gemini)")
            rewritten = generate_least_privilege(policy)
            st.code(rewritten, language="json")

        except Exception as e:
            st.error(f"❌ Error reading policy: {e}")



# --- TAB 2: Kafka Lag Explainer ---
with tab2:
    st.header("📉 Kafka Lag Explainer (AI-Powered)")

    uploaded_csv = st.file_uploader("Upload Kafka lag CSV", type=["csv"])

    if uploaded_csv:
        try:
            df = pd.read_csv(uploaded_csv)
            st.subheader("📄 Uploaded Log")
            st.dataframe(df)

            st.subheader("🧠 AI Risk Assessment")
            findings = analyze_kafka_lag(df)

            for item in findings:
                if "error" in item:
                    st.error(item["error"])
                elif "analysis" in item:
                    st.markdown(item["analysis"])

        except Exception as e:
            st.error(f"❌ Error reading CSV: {e}")

# --- TAB 3: Terraform Risk Summarizer ---
with tab3:
    st.header("📦 Terraform Risk Summarizer")

    uploaded_tf = st.file_uploader("Upload Terraform diff (.txt or .tf)", type=["txt", "tf"])

    if uploaded_tf:
        try:
            diff_text = uploaded_tf.read().decode("utf-8")
            st.subheader("📄 Uploaded Diff")
            st.code(diff_text, language="diff")

            st.subheader("🧠 AI Risk Summary")
            summary = summarize_terraform_diff(diff_text)
            st.markdown(summary)

        except Exception as e:
            st.error(f"❌ Error reading diff: {e}")

# --- TAB 4: Decision Logic Engine ---
with tab4:
    st.header("🧠 Decision Logic Engine")

    uploaded_files = st.file_uploader(
        "Upload any combination of IAM policy (.json), Kafka lag (.csv), or Terraform diff (.txt)",
        type=["json", "csv", "txt"],
        accept_multiple_files=True
    )

    all_issues = []

    for file in uploaded_files:
        filename = file.name.lower()
        try:
            if filename.endswith(".json"):
                import json
                from iam_policy_analyzer.analyzer import analyze_policy
                data = json.load(file)
                all_issues.extend(analyze_policy(data))

            elif filename.endswith(".csv"):
                import pandas as pd
                from kafka_lag_explainer.lag_analyzer import analyze_kafka_lag
                df = pd.read_csv(file)
                all_issues.extend(analyze_kafka_lag(df))

            elif filename.endswith(".txt"):
                from infra_change_summarizer.summarizer import summarize_terraform_diff
                diff_text = file.read().decode("utf-8")
                summary = summarize_terraform_diff(diff_text)
                all_issues.append({
                    "issue": "Terraform diff detected",
                    "details": diff_text,
                    "summary": summary
                })

        except Exception as e:
            st.error(f"Error processing {file.name}: {e}")

    if all_issues:
        st.subheader("🚦 AI-Powered Decision Summary")
        results = assess_risk(all_issues)

        for res in results:
            if "error" in res:
                st.error(res["error"])
                if "raw" in res:
                    st.code(res["raw"])
            else:
                st.markdown(f"**Decision:** `{res['decision']}` | **Risk Score:** `{res['risk_score']}`")
                st.markdown(f"**Reason:** {res['reason']}")
                st.json(res["issue"])

# --- TAB 5: Notifications & Action Generator ---

with tab5:
    st.header("💬 Notifications & Action Generator")

    uploaded_files = st.file_uploader(
        "Upload files again to simulate notifications", 
        type=["json", "csv", "txt"], 
        accept_multiple_files=True
    )

    all_issues = []

    for file in uploaded_files:
        filename = file.name.lower()
        try:
            if filename.endswith(".json"):
                import json
                from iam_policy_analyzer.analyzer import analyze_policy
                data = json.load(file)
                all_issues.extend(analyze_policy(data))

            elif filename.endswith(".csv"):
                import pandas as pd
                from kafka_lag_explainer.lag_analyzer import analyze_kafka_lag
                df = pd.read_csv(file)
                all_issues.extend(analyze_kafka_lag(df))

            elif filename.endswith(".txt"):
                from infra_change_summarizer.summarizer import summarize_terraform_diff
                diff_text = file.read().decode("utf-8")
                summary = summarize_terraform_diff(diff_text)
                all_issues.append({
                    "issue": "Terraform diff detected",
                    "details": diff_text,
                    "summary": summary
                })

        except Exception as e:
            st.error(f"Error processing {file.name}: {e}")

    if all_issues:
        from decision_engine.engine import assess_risk
        decisions = assess_risk(all_issues)

        for d in decisions:
            if "decision" in d:
                note = generate_action_summary(d["issue"], d["decision"])
                render_chat_message(note["title"], note["body"])
            elif "error" in d:
                st.error(d["error"])

st.markdown("---")
st.markdown(
    '<p style="text-align:center;font-size:11px;color:#6b7280;">'
    'Created & developed by <a href="https://linkedin.com/in/phani-marupaka" target="_blank">Phani Marupaka</a>'
    ' · © 2026 All rights reserved.</p>',
    unsafe_allow_html=True
)
