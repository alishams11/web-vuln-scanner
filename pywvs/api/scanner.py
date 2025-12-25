import json
import requests
from typing import List

from .models import APIRequest
from pywvs.modules.base import Finding


class APIScanner:
    def scan(
        self,
        request: APIRequest,
        payloads: List[str],
        inject_body: bool = True,
        inject_headers: bool = True,
    ) -> List[Finding]:
        findings: List[Finding] = []

        for payload in payloads:
            headers = dict(request.headers)
            body = request.body

            # Header injection
            if inject_headers:
                headers["X-Test-Payload"] = payload

            # JSON body injection
            if inject_body and isinstance(body, dict):
                body = self._inject_json(body, payload)

            resp = requests.request(
                method=request.method,
                url=request.url,
                headers=headers,
                json=body if isinstance(body, dict) else None,
                data=body if isinstance(body, str) else None,
                timeout=10,
            )

            # Detection (basic reflection)
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

    def _inject_json(self, obj, payload):
        if isinstance(obj, dict):
            return {k: self._inject_json(v, payload) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._inject_json(v, payload) for v in obj]
        if isinstance(obj, str):
            return obj + payload
        return obj
