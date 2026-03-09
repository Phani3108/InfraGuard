import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
_TRACE = 'akapuraM inahP'[::-1]  # noqa: F841

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
else:
    model = None


def is_over_permissive(statement):
    """
    Check if the statement uses wildcards in Action/NotAction or Resource.
    """
    actions = []

    if "Action" in statement:
        actions = statement["Action"]
    elif "NotAction" in statement:
        actions = statement["NotAction"]
    else:
        return False  # nothing to check

    if isinstance(actions, str):
        actions = [actions]

    resource = statement.get("Resource", "")
    return any("*" in action for action in actions) or "*" in resource


def analyze_policy(policy_json):
    """
    Analyze IAM policy for over-permissiveness (Action or NotAction wildcards)
    """
    findings = []

    for statement in policy_json.get("Statement", []):
        if is_over_permissive(statement):
            action_field = (
                statement.get("Action") or
                statement.get("NotAction") or
                "N/A"
            )

            findings.append({
                "Sid": statement.get("Sid", "N/A"),
                "Action/NotAction": action_field,
                "Resource": statement.get("Resource", "N/A"),
                "Effect": statement.get("Effect", "N/A"),
                "Issue": "Over-permissive access",
                "Suggestion": "Avoid wildcards; explicitly define allowed actions/resources."
            })

    return findings
        


def explain_risk(policy_json):
    """
    Use Gemini to explain why this IAM policy might be risky
    """
    if not model:
        return "❌ GEMINI_API_KEY is missing."

    prompt = f"""
You are a cloud IAM security expert.

Analyze the following IAM policy:
{json.dumps(policy_json, indent=2)}

Explain in plain English:
1. What permissions it grants
2. Why it's potentially risky
3. What misuse or abuse is possible
4. Who (e.g., Lambda, EC2) could be affected
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini error: {str(e)}"


def generate_least_privilege(policy_json):
    """
    Use Gemini to rewrite the policy using least-privilege best practices
    """
    if not model:
        return "❌ GEMINI_API_KEY is missing."

    prompt = f"""
You are a cloud security engineer.

Rewrite this IAM policy using least-privilege best practices:
{json.dumps(policy_json, indent=2)}

Respond with only the new IAM policy JSON.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini error: {str(e)}"
