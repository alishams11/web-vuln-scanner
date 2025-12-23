from typing import List

from pywvs.core_runner import run_wvs_core
from pywvs.templates.engine import TemplateEngine
from pywvs.templates.models import Template
from pywvs.modules.base import Finding


class TemplateScanRunner:
    def __init__(self, concurrency: int = 1):
        self.concurrency = concurrency
        self.engine = TemplateEngine()

    def run(self, template: Template, target: str) -> List[Finding]:
        urls: List[str] = []

        base_url = target.rstrip("/")

        # 1. build URLs from template
        for req in template.requests:
            path = req.path or ""
            if path and not path.startswith("/"):
                path = "/" + path

            base = base_url + path

            if req.payloads:
                for param, payloads in req.payloads.items():
                    for payload in payloads:
                        if f"{{{{{param}}}}}" in base:
                            urls.append(
                                base.replace(f"{{{{{param}}}}}", payload)
                            )
                        else:
                            sep = "&" if "?" in base else "?"
                            urls.append(f"{base}{sep}{param}={payload}")
            else:
                urls.append(base)

        # deduplicate URLs
        urls = list(dict.fromkeys(urls))

        if not urls:
            return []

        print(f"[DEBUG] Built {len(urls)} URLs")

        # 2. run core
        core_results = list(run_wvs_core(urls))
        print(f"[DEBUG] Got {len(core_results)} responses from core")

        # 3. apply template engine
        findings = self.engine.match_core_results(
            template=template,
            target=target,
            core_results=core_results,
        )

        print(f"[DEBUG] Found {len(findings)} findings")
        return findings
