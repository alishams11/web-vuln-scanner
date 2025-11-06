#!/usr/bin/env python3
from pywvs.core_runner import run_wvs_core
import json
import sys

def main():
    urls = [
        "https://example.com",
        "https://httpbin.org/get",
    ]

    print("[*] Running wvs-core (using ./wvs-core binary)...")
    try:
        results = list(run_wvs_core(urls, binary_path="./wvs-core"))
    except Exception as e:
        print(f"[ERROR] running core: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Received {len(results)} responses\n")
    for r in results:
        print(json.dumps(r, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
