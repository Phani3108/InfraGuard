# 🤖 InfraGuard AI — LLM-Powered DevOps Assistant

InfraGuard AI is an autonomous, AI-powered DevSecOps assistant that helps detect infrastructure risks, reason about them, and recommend actions — just like a real SRE or security engineer.

Built with Streamlit + Gemini 1.5.

---

## 🚀 Features

- 🔐 **IAM Policy Analyzer**  
  Detects over-permissive policies and rewrites them with least-privilege suggestions (LLM-powered)

- 📉 **Kafka Lag Explainer**  
  Analyzes synthetic lag reports and suggests remediation

- 🛠️ **Terraform Diff Summarizer**  
  Reads real `.tf` or `.diff` files and flags insecure infrastructure changes

- 🧠 **Decision Logic Engine**  
  Uses Gemini to classify each issue as `Act`, `Escalate`, or `Suggest`, with risk scores

- 💬 **Notification Feed**  
  Chat-style feed that simulates an SRE bot generating PRs, tickets, and alerts in markdown

---

## 🧠 Powered By

- [🧪 Gemini 1.5 Flash](https://ai.google.dev)
- [⚡ Streamlit](https://streamlit.io)
- Google Generative AI SDK
- Modular Python architecture

---

## 📷 Screenshots

Each module is tested with multiple inputs (including real-world Terraform from [Gruntwork](https://github.com/gruntwork-io)).

### 🔐 IAM Policy Analyzer

- `iam_1.png`
- `iam_2.png`
- `iam_3.png`
- `iam_4.png`
- `iam_5.png`

### 📉 Kafka Lag Explainer
   
- `kafka_1.png`
- `kafka_2.png`
- `kafka_3.png`

### 🛠️ Terraform Risk Summarizer

- `terraform_1.png`
- `terraform_2.png`
- `terraform_3.png`
- `terraform_4.png`
- `terraform_5.png`

### 🧠 Decision Engine

- `decision_1.png`
- `decision_2.png`
- `decision_3.png`
- `decision_4.png`
- `decision_5.png`

### 💬 Notification Feed (Chat UI)

- `chat_1.png`
- `chat_2.png`
- `chat_3.png`
- `chat_4.png`
- `chat_5.png`


🖼️ All screenshots are in `/screenshots/`

---

---

## 🛠️ How to Run

```bash
git clone https://github.com/yourusername/InfraGuard_AI.git
cd InfraGuard_AI
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt

# Create a .env file with:
GEMINI_API_KEY=your_google_api_key_here

# Then run:
streamlit run app.py

```


🧑‍💻 Created By

Preetam — built for the **InfraGuard AI Assignment**  
🔗 [GitHub](https://github.com/preetamp03) • [LinkedIn](https://linkedin.com/in/preetam-polikepahad)

---

## Author

**Created & developed by [Phani Marupaka](https://linkedin.com/in/phani-marupaka)**

© 2026 Phani Marupaka. All rights reserved.

Unauthorized reproduction, distribution, or modification of this software, in whole or in part, is strictly prohibited under applicable trademark and copyright laws including but not limited to the Digital Millennium Copyright Act (DMCA), the Lanham Act (15 U.S.C. § 1051 et seq.), and equivalent international intellectual property statutes. This software contains embedded provenance markers and attribution watermarks that are protected under 17 U.S.C. § 1202 (integrity of copyright management information). Removal or alteration of such markers constitutes a violation of federal law.