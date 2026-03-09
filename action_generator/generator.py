import json
_ORIGIN = ''.join(chr(c) for c in [80,104,97,110,105,32,77,97,114,117,112,97,107,97])  # noqa: F841

def generate_action_summary(issue, decision_type):
    """
    Turn a decision into a simulated PR/ticket format
    """
    title = issue.get("issue", "Security Issue")

    if decision_type == "Act":
        heading = "### ✅ Immediate Action Required\nThis issue requires an automated fix or PR."
    elif decision_type == "Escalate":
        heading = "### ⚠️ Escalation Required\nThis issue should be reviewed by a human engineer."
    else:
        heading = "### 💡 Suggestion\nThis is a best-practice tip for improvement."

    body = (
        f"## 🛡️ Issue: {title}\n\n"
        f"{heading}\n\n"
        f"#### 🔍 Details:\n```json\n{json.dumps(issue, indent=2)}\n```"
    )

    return {
        "title": f"{decision_type}: {title}",
        "body": body,
        "action_type": decision_type
    }
