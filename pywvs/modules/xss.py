from typing import List, Dict, Any
from pywvs.modules.base import ScannerModule, Finding
import traceback

# try to reuse legacy scanner utilities if available
try:
    from scanner import form_finder
except Exception:
    form_finder = None

try:
    from scanner import payload_injector
except Exception:
    payload_injector = None


class ReflectedXSSModule(ScannerModule):
    """
    Reflected XSS detection module.

    Modes:
      - Passive (default): looks for common XSS payload echoes / script tags in core_results' body_snippet.
      - Active (config {"active": True}): uses scanner.form_finder + payload_injector to submit payloads to forms.
    """

    name = "xss-reflected"
    description = "Reflected XSS detection (passive + optional active form submission)"
    severity_default = "high"

    # default payload(s) - can be overridden by payload_injector.XSS_PAYLOAD if available
    DEFAULT_PAYLOADS = [
        "<script>alert('XSS')</script>",
        "\"'><script>alert(1)</script>",
        "<svg/onload=alert(1)>",
    ]

    def scan(self, target: str, core_results: List[Dict[str, Any]]) -> List[Finding]:
        findings: List[Finding] = []
        cfg = self.config or {}
        active = bool(cfg.get("active", False))
        payloads = cfg.get("payloads", None) or (
            [getattr(payload_injector, "XSS_PAYLOAD")] if payload_injector and hasattr(payload_injector, "XSS_PAYLOAD") else self.DEFAULT_PAYLOADS
        )

        # PASSIVE detection: look for payload echoes or suspicious script tags
        signatures = [
            "<script",
            "onerror=",
            "<svg/onload",
            "javascript:alert(",
            "document.cookie",
        ]
        # Also check for direct echoes of our payloads
        payload_lowers = [p.lower() for p in payloads]

        for res in core_results:
            body = (res.get("body_snippet") or "").lower()
            url = res.get("url", target)

            # check for direct payload echo
            matched_payload = None
            for p in payload_lowers:
                if p in body:
                    matched_payload = p
                    findings.append(
                        Finding(
                            id="xss-passive-echo",
                            name="Reflected XSS (passive - payload echo)",
                            target=url,
                            severity=self.severity_default,
                            confidence=0.75,
                            evidence={"payload": p, "snippet": (res.get("body_snippet") or "")[:600]},
                            description="Payload appears to be reflected in the response snippet.",
                        )
                    )
                    break

            if matched_payload:
                continue  # one finding per response is enough for passive

            # check generic script-like signatures
            for sig in signatures:
                if sig in body:
                    findings.append(
                        Finding(
                            id="xss-passive-signature",
                            name="Possible reflected/script-like content (passive)",
                            target=url,
                            severity=self.severity_default,
                            confidence=0.45,
                            evidence={"signature": sig, "snippet": (res.get("body_snippet") or "")[:400]},
                            description="Suspicious script-like content found in response snippet.",
                        )
                    )
                    break

        # ACTIVE detection: submit payloads to discovered forms (only if allowed by config)
        if active and form_finder and payload_injector:
            try:
                forms = form_finder.find_forms(target)
            except Exception:
                forms = []

            for details in forms:
                for payload in payloads:
                    try:
                        resp = payload_injector.submit_form(details, target, payload, vulnerable_type="xss")
                        if payload_injector.is_vulnerable(resp, payload):
                            findings.append(
                                Finding(
                                    id="xss-active-form",
                                    name="Reflected XSS (active - form submission)",
                                    target=target,
                                    severity=self.severity_default,
                                    confidence=0.9,
                                    evidence={
                                        "form": details,
                                        "payload": payload,
                                        "response_snippet": (resp.text or "")[:600] if resp is not None else "",
                                    },
                                    description="Active form submission reflected the payload in the response.",
                                )
                            )
                            # stop further payloads for this form (we found it)
                            break
                    except Exception:
                        # don't let legacy code crash the module
                        traceback.print_exc()
                        continue

        return findings
