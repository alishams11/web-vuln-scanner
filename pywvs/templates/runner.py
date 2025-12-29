from typing import List
from pathlib import Path

from pywvs.core_runner import run_wvs_core
from pywvs.templates.engine import TemplateEngine
from pywvs.templates.models import Template
from pywvs.modules.base import Finding
from pywvs.auth.session import AuthSession

from pywvs.ignore.loader import load_ignore_file
from pywvs.ignore.matcher import is_ignored


class TemplateScanRunner:

    def __init__(
        self,
        concurrency: int = 1,
        auth_session: AuthSession | None = None,
        ignore_file: str = ".wvs-ignore",
    ):
        self.concurrency = concurrency
        self.auth_session = auth_session
        self.engine = TemplateEngine()
        self.ignore_file = ignore_file

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
                            urls.append(base.replace(f"{{{{{param}}}}}", payload))
                        else:
                            sep = "&" if "?" in base else "?"
                            urls.append(f"{base}{sep}{param}={payload}")
            else:
                urls.append(base)

        # deduplicate
        urls = list(dict.fromkeys(urls))
        if not urls:
            return []

        print(f"[DEBUG] Built {len(urls)} URLs")

        # 2. fetch responses
        if self.auth_session:
            core_results = []
            for url in urls:
                r = self.auth_session.request("GET", url)
                core_results.append(
                    {
                        "url": url,
                        "status_code": r.status_code,
                        "headers": dict(r.headers),
                        "body_snippet": r.text[:2000],
                    }
                )
        else:
            core_results = list(run_wvs_core(urls))

        print(f"[DEBUG] Got {len(core_results)} responses")

        # 3. apply template engine
        findings = self.engine.match_core_results(
            template=template,
            target=target,
            core_results=core_results,
        )

        print(f"[DEBUG] Found {len(findings)} findings (before ignore)")

        # 4. load ignore rules
        ignore_path = Path(self.ignore_file)
        ignore_rules = load_ignore_file(ignore_path)

        if ignore_rules:
            print(f"[DEBUG] Loaded {len(ignore_rules)} ignore rules from {ignore_path}")

        # 5. apply ignore filtering
        final_findings: List[Finding] = []
        for finding in findings:
            if is_ignored(finding, ignore_rules):
                print(
                    f"[DEBUG] Ignored finding {finding.id} "
                    f"(confidence={finding.confidence})"
                )
                continue
            final_findings.append(finding)

        print(f"[DEBUG] Remaining {len(final_findings)} findings (after ignore)")
        return final_findings
