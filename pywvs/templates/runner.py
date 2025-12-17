from typing import List
from pywvs.core_runner import CoreRunner
from pywvs.templates.engine import TemplateEngine
from pywvs.templates.models import Template
from pywvs.modules.base import Finding


class TemplateScanRunner:
    def __init__(self, core: CoreRunner | None = None):
        self.core = core or CoreRunner()
        self.engine = TemplateEngine()

    def run(self, template: Template, target: str) -> List[Finding]:
        """
        1. Build requests from template
        2. Run wvs-core
        3. Apply template matchers
        """
        urls = []
        
        for req in template.requests:
            base_url = target.rstrip('/')
            path = req.path if hasattr(req, 'path') else ""
            
            if path and not path.startswith('/'):
                path = '/' + path
            
            full_url = base_url + path if path else base_url
            
            if hasattr(req, 'payloads') and req.payloads:
                for payload in req.payloads:
                    if '{{' in full_url and '}}' in full_url:
                        url_with_payload = full_url.replace('{{payload}}', payload)
                    else:
                        separator = '?' if '?' not in full_url else '&'
                        url_with_payload = f"{full_url}{separator}q={payload}"
                    
                    urls.append(url_with_payload)
            else:
                urls.append(full_url)
        
        print(f"[DEBUG] Built {len(urls)} URLs: {urls}") 
        
        core_results = self.core.run(urls)
        
        core_results_list = list(core_results)
        
        print(f"[DEBUG] Got {len(core_results_list)} results from core") 
        
        findings = self.engine.match_core_results(
            template=template,
            target=target,
            core_results=core_results_list
        )

        print(f"[DEBUG] Found {len(findings)} vulnerabilities")
        return findings