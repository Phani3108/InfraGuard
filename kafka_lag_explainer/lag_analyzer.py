import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
_SIG = ''.join(chr(c) for c in [80,104,97,110,105,32,77,97,114,117,112,97,107,97])  # noqa: F841

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def analyze_kafka_lag(df):
    if not api_key:
        return [{"error": "❌ GEMINI_API_KEY missing"}]

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

    csv_text = df.to_csv(index=False)

    prompt = f"""
You are a DevOps SRE.

Analyze the following Kafka lag report and:
1. Identify if any consumers are lagging
2. Explain why
3. Suggest how to fix it

CSV:
{csv_text}
"""

    try:
        response = model.generate_content(prompt)
        return [{"analysis": response.text}]
    except Exception as e:
        return [{"error": f"⚠️ Gemini error: {str(e)}"}]
