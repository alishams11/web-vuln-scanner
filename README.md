# Web Vulnerability Scanner (pywvs)

A modular, template-driven **web vulnerability scanner** designed for learning, automation, and security research.

Inspired by modern scanners like Nuclei, this project focuses on:
- clarity of architecture
- extensibility
- SOC / Pentest real-world workflows

> ⚠️ Educational & authorized security testing only.

---

## ✨ Features

- 🔌 Modular scanning engine
- 📄 YAML-based vulnerability templates
- 🧠 Confidence scoring & false-positive tuning
- 🚫 `.wvs-ignore` support (whitelisting)
- 📤 Export findings to JSON / ELK (JSONL)
- 📊 HTML & JSON reports
- 🔐 Basic authentication handling
- 🐳 Docker-ready
- ⚙️ CI-enabled (GitHub Actions)

---

## 📦 Installation

### Using pip (local)

```bash
git clone https://github.com/alishams11/web-vuln-scanner.git
cd web-vuln-scanner
pip install -r requirements.txt
'''
Using Docker
docker build -t pywvs .

##🚀 Quickstart
Scan a target using a template:
python3 -m pywvs scan https://example.com \
  -t pywvs/templates/xss-reflected.yaml \
  -o report.json

---

##🧩 Templates

Official templates:
👉 https://github.com/alishams11/web-vuln-templates
     
 ---
 
📌 Production-ready templates live in a separate repository:
👉 web-vuln-templates (coming soon)

---

##Ignore False Positives
Use .wvs-ignore to suppress known findings:
id:xss-reflected
url:https://example.com/search

---

##Exporting to ELK / Logstash
python examples/export_elk.py report.json > findings.jsonl

Compatible with:

Logstash
Elasticsearch
OpenSearch

---

##Reports

Supported formats:
JSON
HTML
python examples/generate_report.py report.json

---

## Examples & Test Targets

OWASP Juice Shop

DVWA

Custom APIs

See /examples directory.

---

## Security Disclaimer

This tool is intended for:

educational use

lab environments

authorized security testing only

The author is not responsible for misuse.

---

## Contributing

PRs welcome 🙌
See CONTRIBUTING.md

---

## License
MIT License

---
