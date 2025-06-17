# 🔍 Web Vulnerability Scanner

A simple Python-based CLI tool to scan web pages for **XSS** and **SQL Injection** vulnerabilities by detecting HTML forms and injecting test payloads.

![CLI Demo](screenshots/cli_demo.png)

---

## 🚀 Features

- ✅ Detects HTML forms on a given web page
- ✅ Extracts method, action, and inputs
- ✅ Automatically injects XSS and SQLi payloads
- ✅ Checks for reflections or error-based indications
- ✅ Saves findings in `outputs/results.json` with timestamps

---

## ⚙️ Installation

```bash
git clone https://github.com/alishams11/web-vuln-scanner.git
cd web-vuln-scanner
pip3 install -r requirements.txt


#🕹️ Usage

python3 main.py -u http://target.com

#📝 Sample Output

[
  {
    "timestamp": "2025-06-17 12:52:49",
    "vulnerability": "XSS",
    "target": "http://testphp.vulnweb.com/",
    "payload": "<script>alert('XSS')</script>"
  }
]

#📁 Output

All results are saved in:

outputs/results.json

#📸 Screenshot
screenshots/cli_demo.png
