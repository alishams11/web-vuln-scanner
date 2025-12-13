import re
import subprocess
import json
from typing import List

from .models import Template, Matcher
from pywvs.modules.base import Finding


class TemplateEngine:
    def run(self, template: Template, target: str) -> List[Finding]:
        findings: List[Finding] = []

        for req in template.requests:
            for param, payloads in req.payloads.items():
                for payload in payloads:
                    url = target + req.path.replace(f"{{{{{param}}}}}", payload)

                    resp = self._fetch(url)
                    if not resp:
                        continue

                    if self._match(resp, template.matchers):
                        findings.append(
                            Finding(
                                id=template.id,
                                name=template.name,
                                target=url,
                                severity=template.severity,
                                confidence=0.9,
                                evidence={"payload": payload},
                            )
                        )

        return findings

    def _fetch(self, url: str) -> dict | None:
        """
        Call wvs-core and return first JSON response
        """
        try:
            proc = subprocess.run(
                ["./wvs-core", url],
                capture_output=True,
                text=True,
                check=True,
            )
            line = proc.stdout.strip().splitlines()
            return json.loads(line[0]) if line else None
        except Exception:
            return None

    def _match(self, resp: dict, matchers: List[Matcher]) -> bool:
        """
        All matchers must match (AND logic)
        """
        for m in matchers:
            if m.type == "word":
                body = resp.get("body_snippet", "")
                if not m.words or not any(w in body for w in m.words):
                    return False

            elif m.type == "regex":
                body = resp.get("body_snippet", "")
                if not m.regex or not any(re.search(r, body) for r in m.regex):
                    return False

            elif m.type == "status":
                if resp.get("status_code") not in (m.status or []):
                    return False

            elif m.type == "header":
                headers = resp.get("headers", {})
                if not m.words:
                    return False
                found = any(
                    any(w.lower() in v.lower() for v in values)
                    for values in headers.values()
                    for w in m.words
                )
                if not found:
                    return False

            else:
                # unknown matcher
                return False

        return True
