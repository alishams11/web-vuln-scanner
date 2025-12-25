import requests
from typing import List

from pywvs.modules.base import Finding
from pywvs.auth.session import AuthSession
from pywvs.api.models import APIRequest


class APIScanner:
   

    def __init__(self, session: AuthSession | None = None):
        self.session = session.session if session else requests.Session()

    def scan(
        self,
        request: APIRequest,
        payloads: List[str],
    ) -> List[Finding]:
        findings: List[Finding] = []

        for payload in payloads:
            data = request.body
            if isinstance(data, dict):
                data = data.copy()
                for k in data:
                    data[k] = payload

            resp = self.session.request(
                request.method,
                request.url,
                headers=request.headers,
                json=data,
            )

            if payload in resp.text:
                findings.append(
                    Finding(
                        id="api-reflection",
                        name="API Payload Reflection",
                        target=request.url,
                        severity="medium",
                        confidence=0.8,
                        evidence={
                            "payload": payload,
                            "status": resp.status_code,
                        },
                    )
                )

        return findings
