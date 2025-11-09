#!/usr/bin/env python3
from pywvs.core_runner import run_wvs_core
from pywvs.modules import XSSModule, SQLiModule
import json

def main():
    urls = [
        "https://example.com",
        "https://httpbin.org/get",
    ]

    # run core and gather results
    print("[*] running core...")
    core_results = list(run_wvs_core(urls, binary_path="./wvs-core"))

    # instantiate modules
    xss = XSSModule()
    sqli = SQLiModule()

    # group results per target if needed; here core returns per-request
    # we'll pass the whole core_results to each scan for simplicity
    findings = []
    findings.extend(xss.scan(urls[0], core_results))
    findings.extend(sqli.scan(urls[0], core_results))

    print(f"[*] Findings: {len(findings)}")
    for f in findings:
        print(json.dumps(f.__dict__, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
