from typing import List
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from pywvs.modules.base import Finding
from .base import Reporter


class HTMLReporter(Reporter):
    def __init__(self):
        templates_dir = Path(__file__).parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(["html"]),
        )

    def generate(self, findings: List[Finding], output_path: str) -> None:
        template = self.env.get_template("report.html.j2")

        html = template.render(
            findings=findings,
            summary=self._summary(findings),
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

    def _summary(self, findings: List[Finding]) -> dict:
        s = {}
        for f in findings:
            s[f.severity] = s.get(f.severity, 0) + 1
        return {
            "total": len(findings),
            "by_severity": s,
        }
