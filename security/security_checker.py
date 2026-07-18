"""
Basic static security inspection.

This is NOT a replacement for Bandit or Semgrep.

Its goal is to warn the user before sending code to the LLM.
"""

import re

SECURITY_RULES = {

    "SQL Injection":
        r"SELECT.+\+|INSERT.+\+|UPDATE.+\+|DELETE.+\+",

    "Command Injection":
        r"os\.system|subprocess\.Popen|subprocess\.call",

    "Hardcoded Secret":
        r"(password|secret|token|apikey)\s*=\s*['\"]",

    "Eval Usage":
        r"\beval\s*\(",

    "Exec Usage":
        r"\bexec\s*\(",

    "Pickle Usage":
        r"pickle\.loads",

    "YAML Unsafe Load":
        r"yaml\.load",

    "Shell=True":
        r"shell\s*=\s*True",

    "Weak Random":
        r"random\.random",

}


def scan_security(code: str):

    findings = []

    for issue, pattern in SECURITY_RULES.items():

        if re.search(pattern, code, re.IGNORECASE | re.DOTALL):

            findings.append(issue)

    return findings


def security_summary(code: str):

    findings = scan_security(code)

    if not findings:

        return (
            True,
            "No obvious security problems detected."
        )

    return (
        False,
        "\n".join(findings),
    )