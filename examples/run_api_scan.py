from pywvs.api.loader import load_api_request
from pywvs.api.scanner import APIScanner

req = load_api_request("examples/api_request.json")

scanner = APIScanner()
findings = scanner.scan(
    req,
    payloads=["<script>alert(1)</script>", "' OR 1=1 --"]
)

for f in findings:
    print(f)
