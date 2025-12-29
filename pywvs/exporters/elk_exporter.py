import json
from datetime import datetime
from typing import List

from pywvs.modules.base import Finding
from .base import BaseExporter


class ELKExporter(BaseExporter):
    """
    Export findings in JSON Lines format (one finding per line)
    Compatible with ELK / Logstash / Filebeat
    """

    def export(self, findings: List[Finding], output_path: str) -> None:
        with open(output_path, "w", encoding="utf-8") as f:
            for finding in findings:
                record = {
                    "@timestamp": datetime.utcnow().isoformat() + "Z",
                    "scanner": "web-vuln-scanner",
                    "finding": {
                        "id": finding.id,
                        "name": finding.name,
                        "severity": finding.severity,
                        "confidence": finding.confidence,
                        "target": finding.target,
                        "evidence": finding.evidence,
                        "description": finding.description,
                    },
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
