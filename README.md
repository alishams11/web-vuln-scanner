# Web Vulnerability Scanner (pywvs)

A modular, template-driven **web vulnerability scanner** designed for learning,
automation, and security research.

Inspired by modern scanners like **Nuclei**, with focus on:
- Clean architecture
- High extensibility
- Real-world SOC / Pentest workflows

> ⚠️ For educational and **authorized security testing only**.

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

Official templates repository:
👉 https://github.com/alishams11/web-vuln-templates

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

## 📜 License

MIT License
