from typing import List, Dict, Any
from pywvs.modules.base import ScannerModule, Finding
import traceback

try:
    from scanner import payload_injector
except Exception:
    payload_injector = None

SQL_ERROR_SIGS = [
    "you have an error in your sql syntax",
    "mysql_fetch_assoc(",
    "syntax error at or near",
    "unclosed quotation mark after the character string",
    "pg::syntaxerror",
    "sql syntax",
    "mysql error",
    "odbc",
]


class SQLiAdapter(ScannerModule):
    name = "sqli-adapter"
    description = "Adapter wrapping legacy SQLi checks (passive by default, optional active)"
    severity_default = "medium"

    def scan(self, target: str, core_results: List[Dict[str, Any]]) -> List[Finding]:
        findings: List[Finding] = []
        cfg = self.config or {}
        active = bool(cfg.get("active", False))

        # PASSIVE
        for res in core_results:
            body = (res.get("body_snippet") or "").lower()
            url = res.get("url", target)
            for sig in SQL_ERROR_SIGS:
                if sig in body:
                    findings.append(
                        Finding(
                            id="sqli-passive-001",
                            name="Potential SQLi (passive - error-based)",
                            target=url,
                            severity=self.severity_default,
                            confidence=0.65,
                            evidence={"signature": sig, "snippet": (res.get("body_snippet") or "")[:400]},
                            description="Passive detection of a database error signature in the response.",
                        )
                    )
                    break

        # ACTIVE (forms)
        if active and payload_injector:
            try:
                from scanner import form_finder
            except Exception:
                form_finder = None

            if form_finder:
                try:
                    forms = form_finder.find_forms(target)
                except Exception:
                    forms = []
                for details in forms:
                    try:
                        resp = payload_injector.submit_form(details, target, payload_injector.SQLI_PAYLOAD, vulnerable_type="sqli")
                        if payload_injector.is_vulnerable(resp, payload_injector.SQLI_PAYLOAD):
                            findings.append(
                                Finding(
                                    id="sqli-active-001",
                                    name="Potential SQLi (active)",
                                    target=target,
                                    severity=self.severity_default,
                                    confidence=0.85,
                                    evidence={
                                        "form": details,
                                        "payload": getattr(payload_injector, "SQLI_PAYLOAD", "' OR '1'='1"),
                                        "response_snippet": (resp.text or "")[:400] if resp is not None else "",
                                    },
                                )
                            )
                    except Exception:
                        traceback.print_exc()
                        continue

        return findings
