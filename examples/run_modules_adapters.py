#!/usr/bin/env python3
from pywvs.core_runner import run_wvs_core
from pywvs.modules import XSSAdapter, SQLiAdapter
import json
import sys

def main():
    urls = ["https://example.com", "https://httpbin.org/get"]
    core_results = list(run_wvs_core(urls, binary_path="./wvs-core"))

    x = XSSAdapter(config={"active": False})
    s = SQLiAdapter(config={"active": False})

    findings = []
    findings.extend(x.scan(urls[0], core_results))
    findings.extend(s.scan(urls[0], core_results))

    print(json.dumps([f.__dict__ for f in findings], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
