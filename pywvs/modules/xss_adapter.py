from typing import List, Dict, Any
from pywvs.modules.base import ScannerModule, Finding
import traceback

try:
    from scanner import form_finder
except Exception:
    form_finder = None

try:
    from scanner import payload_injector
except Exception:
    payload_injector = None


class XSSAdapter(ScannerModule):
    name = "xss-adapter"
    description = "Adapter wrapping legacy form-based XSS checks (passive by default, optional active)"
    severity_default = "high"

    def scan(self, target: str, core_results: List[Dict[str, Any]]) -> List[Finding]:
        findings: List[Finding] = []
        cfg = self.config or {}
        active = bool(cfg.get("active", False))

        # PASSIVE
        payload_signatures = [
            "<script>alert(",
            "onerror=",
            "<svg/onload",
            "javascript:alert(",
            "<iframe",
        ]

        for res in core_results:
            body = (res.get("body_snippet") or "").lower()
            url = res.get("url", target)
            for sig in payload_signatures:
                if sig in body:
                    findings.append(
                        Finding(
                            id="xss-passive-001",
                            name="Possible reflected XSS (passive)",
                            target=url,
                            severity=self.severity_default,
                            confidence=0.6,
                            evidence={"signature": sig, "snippet": (res.get("body_snippet") or "")[:400]},
                            description="Passive heuristic found script-like signature in response snippet.",
                        )
                    )
                    break

        # ACTIVE: use legacy form_finder + payload_injector
        if active and form_finder and payload_injector:
            try:
                forms = form_finder.find_forms(target)
            except Exception:
                forms = []
            for details in forms:
                try:
                    resp = payload_injector.submit_form(details, target, payload_injector.XSS_PAYLOAD, vulnerable_type="xss")
                    if payload_injector.is_vulnerable(resp, payload_injector.XSS_PAYLOAD):
                        findings.append(
                            Finding(
                                id="xss-active-001",
                                name="Reflected XSS (active)",
                                target=target,
                                severity=self.severity_default,
                                confidence=0.9,
                                evidence={
                                    "form": details,
                                    "payload": getattr(payload_injector, "XSS_PAYLOAD", "<payload>"),
                                    "response_snippet": (resp.text or "")[:400] if resp is not None else "",
                                },
                                description="Active form submission returned payload in response.",
                            )
                        )
                except Exception:
                    traceback.print_exc()
                    continue

        return findings
