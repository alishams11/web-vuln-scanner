import json
from typing import List
from pywvs.modules.base import Finding
from .base import Reporter


class JSONReporter(Reporter):
    def generate(self, findings: List[Finding], output_path: str) -> None:
        data = {
            "summary": {
                "total": len(findings),
                "by_severity": self._severity_stats(findings),
            },
            "findings": [self._serialize(f) for f in findings],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _serialize(self, f: Finding) -> dict:
        return {
            "id": f.id,
            "name": f.name,
            "target": f.target,
            "severity": f.severity,
            "confidence": f.confidence,
            "description": f.description,
            "evidence": f.evidence,
        }

    def _severity_stats(self, findings: List[Finding]) -> dict:
        stats = {}
        for f in findings:
            stats[f.severity] = stats.get(f.severity, 0) + 1
        return stats
