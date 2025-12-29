from pywvs.exporters.elk_exporter import ELKExporter
from pywvs.modules.base import Finding

findings = [
    Finding(
        id="xss-reflected",
        name="Reflected XSS",
        target="https://example.com?q=<script>",
        severity="high",
        confidence=0.9,
        evidence={"payload": "<script>alert(1)</script>"},
    )
]

ELKExporter().export(findings, "elk-findings.jsonl")
print("[+] ELK JSONL generated")
