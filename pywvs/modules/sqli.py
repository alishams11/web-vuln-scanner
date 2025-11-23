from __future__ import annotations
from typing import List, Dict, Any
from .base import ScannerModule, Finding


SQL_ERRORS = [
    "you have an error in your sql syntax;",
    "unclosed quotation mark after the character string",
    "quoted string not properly terminated",
    "mysql_fetch_array()",
    "mysql_num_rows()",
    "syntax error at or near",
    "sqlite error",
    "unknown column",
    "warning: mysql",
    "sqlstate[",
    "pg_query():",
]


class SQLiPassiveModule(ScannerModule):
    name = "sqli_passive"
    description = "Passive SQL Injection detection based on error patterns"
    severity_default = "medium"

    def scan(self, target: str, core_results: List[Dict[str, Any]]) -> List[Finding]:
        findings = []

        for entry in core_results:
            url = entry.get("url", "")
            body = entry.get("body", "").lower() if entry.get("body") else ""

            # check SQL error signatures
            for err in SQL_ERRORS:
                if err in body:
                    findings.append(
                        Finding(
                            id=f"sqli-passive-{hash(url + err)}",
                            name="SQL Injection (Passive Error-Based)",
                            target=url,
                            severity="medium",
                            confidence=0.8,
                            evidence={"error": err, "snippet": body[:200]},
                            description=f"Detected SQL error message in response body: '{err}'.",
                        )
                    )
                    break  # one finding per URL is enough

        return findings
