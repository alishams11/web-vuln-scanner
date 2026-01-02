# Web Vulnerability Scanner (pywvs)

A **template-driven, detection-oriented web vulnerability scanner**
designed for **security engineers and pentesters** who care about
**accuracy, context, and reportable findings** — not just raw scanning.

Inspired by tools like **Nuclei**, but built with a stronger focus on:
- Detection logic & confidence scoring
- False-positive reduction
- SOC / AppSec / Pentest integration workflows

> ⚠️ For educational and **authorized security testing only**.

---
##🧠 Why This Project?

Most web scanners focus on speed and volume, often producing noisy results
that are hard to trust or report.

This project aims to:

Bridge the gap between pentest tools and security engineering needs

Provide explainable findings with evidence and confidence

Support real-world workflows such as SIEM ingestion and reporting

Encourage template-driven detection logic instead of hardcoded checks

---

##✨ Features

🔌 Modular scanning engine (extensible by design)

📄 YAML-based vulnerability templates (request + matcher logic)

🧠 Confidence scoring to reduce false positives

🚫 .wvs-ignore support for whitelisting known issues

📤 Export findings to JSON / ELK-compatible JSONL

📊 HTML & JSON reports with evidence

🔐 Basic authentication & session handling

🐳 Docker-ready for lab and CI usage

⚙️ CI-enabled (GitHub Actions)
---
##🏗️ High-Level Architecture
Target URLs
    ↓
Core Scan Engine
    ↓
Template Requests (YAML)
    ↓
Matchers & Detection Logic
    ↓
Findings (severity, confidence, evidence)
    ↓
Reporters (JSON / HTML / ELK)

---
## 📦 Installation

### Local installation (pip)

```bash
git clone https://github.com/alishams11/web-vuln-scanner.git
cd web-vuln-scanner
pip install -r requirements.txt
```

### Using Docker

```bash
docker build -t pywvs .
```

---

## 🚀 Quick Start

```bash
python3 -m pywvs scan https://example.com \
  -t pywvs/templates/xss-reflected.yaml \
  -o report.json
```

---

## 🧩 Templates

Detection logic is defined using YAML templates.

👉Official templates repository:https://github.com/alishams11/web-vuln-templates
Templates define:

Requests to send

Matchers to evaluate responses

Severity and metadata

This separation allows:

Easier tuning

Community-driven rules

Clear auditability of detections
---

## 🚫 Ignore False Positives

```text
id: xss-reflected
url: https://example.com/search
```

---

## 📤 Exporting to ELK / Logstash

```bash
python examples/export_elk.py report.json > findings.jsonl
```

Compatible with:
- Logstash
- Elasticsearch
- OpenSearch

---

## 📊 Reports

```bash
python examples/generate_report.py report.json
```

---

## ⚠️ Security Disclaimer

Educational and authorized testing only.

---
##🧭 Roadmap (High-Level)

API scanning support

Advanced authentication flows

Additional vulnerability templates

Detection tuning & confidence improvements

---
##🎯 Intended Audience

Security Engineers

Application Security (AppSec)

Pentesters

Blue Team / SOC learners

---
## 📜 License

MIT License
