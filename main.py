import argparse
import os
import json
from datetime import datetime
from scanner.form_finder import find_forms
from scanner.payload_injector import submit_form, is_vulnerable, XSS_PAYLOAD, SQLI_PAYLOAD

def get_args():
    parser = argparse.ArgumentParser(description="Web Vulnerability Scanner (XSS + SQLi)")
    parser.add_argument("-u", "--url", required=True, help="Target URL to scan")
    return parser.parse_args()


def save_result(vuln_type, url, payload):
    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "vulnerability": vuln_type,
        "target": url,
        "payload": payload
    }

    output_file = "outputs/results.json"
    os.makedirs("outputs", exist_ok=True)

    if not os.path.exists(output_file) or os.stat(output_file).st_size == 0:
        results = []
    else:
        with open(output_file, "r") as f:
            results = json.load(f)

    results.append(report)

    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
        
if __name__ == "__main__":
    args = get_args()
    url = args.url
    forms = find_forms(url) 

    for form in forms:
        for payload, payload_type in [(XSS_PAYLOAD, "XSS"), (SQLI_PAYLOAD, "SQLi")]:
            response = submit_form(form, url, payload, payload_type)
            if is_vulnerable(response, payload):
                 print(f"🔥 [VULNERABLE] {payload_type} vulnerability detected!")
                 save_result(payload_type, url, payload)
            else:
                print(f"✅ [{payload_type}] Not vulnerable.")
