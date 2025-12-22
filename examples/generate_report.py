from pywvs.reporters.json_reporter import JSONReporter
from pywvs.reporters.html_reporter import HTMLReporter
from pywvs.modules.base import Finding

findings = [
    Finding(
        id="XSS-001",
        name="Reflected XSS",
        target="https://example.com?q=<script>",
        severity="high",
        confidence=0.9,
        evidence={"payload": "<script>alert(1)</script>"},
    )
]

JSONReporter().generate(findings, "examples/report.json")
HTMLReporter().generate(findings, "examples/report.html")

print("[+] Reports generated")
