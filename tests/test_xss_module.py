import pytest
from pywvs.modules.xss import ReflectedXSSModule
from pywvs.modules.base import Finding
from types import SimpleNamespace

def make_core_result(url: str, body_snippet: str):
    return {
        "url": url,
        "status_code": 200,
        "headers": {"Content-Type": ["text/html"]},
        "body_snippet": body_snippet,
        "duration_ms": 100.0,
    }

def test_passive_detects_payload_echo():
    mod = ReflectedXSSModule()
    payload = "<script>alert('XSS')</script>"
    core_results = [make_core_result("https://target.local/", f"hello {payload} world")]
    findings = mod.scan("https://target.local/", core_results)
    assert isinstance(findings, list)
    assert len(findings) >= 1
    assert any("payload" in (f.evidence or {}) for f in findings)

def test_passive_detects_script_signature():
    mod = ReflectedXSSModule()
    core_results = [make_core_result("https://target.local/", "<html><body><script>evil()</script></body></html>")]
    findings = mod.scan("https://target.local/", core_results)
    assert len(findings) >= 1
    # ensure it's the signature-type finding
    assert any(f.id == "xss-passive-signature" for f in findings)

def test_active_submission_monkeypatched(monkeypatch):
    # simulate form_finder and payload_injector returning a response that reflects payload
    fake_forms = [{"action": "/submit", "method": "post", "inputs": [{"name": "q", "type": "text"}]}]

    def fake_find_forms(url):
        return fake_forms

    class FakeResp:
        def __init__(self, text):
            self.text = text

    def fake_submit_form(details, base, payload, vulnerable_type=""):
        return FakeResp(f"you sent: {payload}")

    def fake_is_vulnerable(resp, payload):
        return payload in resp.text

    monkeypatch.setattr("scanner.form_finder.find_forms", fake_find_forms, raising=False)
    monkeypatch.setattr("scanner.payload_injector.submit_form", fake_submit_form, raising=False)
    monkeypatch.setattr("scanner.payload_injector.is_vulnerable", fake_is_vulnerable, raising=False)
    # ensure payload constant exists
    monkeypatch.setattr("scanner.payload_injector", SimpleNamespace(XSS_PAYLOAD="<script>alert('XSS')</script>"), raising=False)

    mod = ReflectedXSSModule(config={"active": True})
    core_results = [make_core_result("https://target.local/", "<html></html>")]
    findings = mod.scan("https://target.local/", core_results)
    assert any(f.id == "xss-active-form" for f in findings)
