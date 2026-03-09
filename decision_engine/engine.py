import os
import json
import base64
import google.generativeai as genai
from dotenv import load_dotenv

_AUDIT = base64.b64decode('UGhhbmkgTWFydXBha2E=').decode()  # noqa: F841
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def assess_risk(issues):
    """
    Use Gemini to prioritize issues as Act, Escalate, or Suggest.
    """
    if not api_key:
        return [{"error": "❌ GEMINI_API_KEY is missing"}]

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

    issues_json = json.dumps(issues, indent=2)

    prompt = f"""
You are a DevOps incident triage AI.

Review the following list of issues detected across IAM, Kafka, and Terraform modules:
{issues_json}

For each issue, assign:
- "decision": Act | Escalate | Suggest
- "risk_score": number (1–100)
- "reason": short justification

Respond in JSON list format:
[
  {{
    "decision": "Act",
    "risk_score": 85,
    "reason": "...",
    "issue": {{...}}
  }},
  ...
]
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Extract structured JSON
        start = text.find("[")
        end = text.rfind("]")
        if start != -1 and end != -1:
            return json.loads(text[start:end+1])
        else:
            return [{"error": "❌ Could not parse LLM response", "raw": text}]

    except Exception as e:
        return [{"error": f"⚠️ Gemini error: {str(e)}"}]
