import re
from typing import List, Dict

from pywvs.modules.base import Finding
from .models import Template, Matcher


class TemplateEngine:
    """
    Template matcher engine.

    This class does NOT perform any network requests.
    It only applies matchers on core results.
    """

    def match_core_results(
        self,
        template: Template,
        target: str,
        core_results: List[Dict],
    ) -> List[Finding]:
        findings: List[Finding] = []

        for resp in core_results:
            if self._match(resp, template.matchers):
                findings.append(
                    Finding(
                        id=template.id,
                        name=template.name,
                        target=resp.get("url", target),
                        severity=template.severity,
                        confidence=0.8,
                        evidence={
                            "status": resp.get("status_code"),
                            "matched": True,
                        },
                    )
                )

        return findings

    def _match(self, resp: Dict, matchers: List[Matcher]) -> bool:
        """
        AND logic: all matchers must match
        """
        for m in matchers:
            body = resp.get("body_snippet", "")
            headers = resp.get("headers", {})
            status = resp.get("status_code")

            if m.type == "word":
                if not m.words or not any(w in body for w in m.words):
                    return False

            elif m.type == "regex":
                if not m.regex or not any(re.search(r, body) for r in m.regex):
                    return False

            elif m.type == "status":
                if status not in (m.status or []):
                    return False

            elif m.type == "header":
                if not m.words:
                    return False
                found = any(
                    any(w.lower() in v.lower() for w in m.words)
                    for values in headers.values()
                    for v in values
                )
                if not found:
                    return False

            else:
                # unknown matcher type
                return False

        return True
