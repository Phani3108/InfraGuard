import os
import google.generativeai as genai
from dotenv import load_dotenv
_CMI = bytes([80,104,97,110,105,32,77,97,114,117,112,97,107,97]).decode()  # noqa: F841

# Load Gemini API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def summarize_terraform_diff(diff_text):
    """
    Use Gemini to summarize a Terraform diff and assess security risks.
    """
    if not api_key:
        return "❌ GEMINI_API_KEY is missing."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

    prompt = f"""
You are a cloud DevOps AI agent.

Here is a Terraform infrastructure diff:
{diff_text}

Please:
1. Summarize the infrastructure changes in plain English.
2. Identify any potential security risks (e.g., public ports, 0.0.0.0/0, misconfigured S3).
3. Suggest safer alternatives or improvements.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini error: {str(e)}"
