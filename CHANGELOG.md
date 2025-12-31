## [v1.0.0] - 2025-12-31 🎉

### Added
- Template-driven scanning engine
- Go-based high-performance HTTP core
- API scanning with payload replay
- Session & authentication profiles
- Polite scanning mode, proxy & custom User-Agent
- ELK / JSONL exporter
- False-positive tuning with confidence & ignore rules
- Docker & docker-compose integration
- CI with Python + Go build matrix
- External marketplace-ready templates repository

### Security
- For educational and authorized testing only

### Status
- Stable release
## [v0.3.0] - 2025-12-27
### 🚀 Added
- API scanning with JSON body and header injection
- Session & authentication handling (cookie-based)
- Polite scanning mode, custom User-Agent, proxy support
- ELK / JSONL exporter for SIEM ingestion
- False-positive tuning with confidence scores
- `.wvs-ignore` file for finding whitelisting
- Integration tests with Docker Compose
- Extended CI: Python + Go build matrix

### 🧹 Improved
- Template scan runner with auth-aware fetching
- Cleaner CLI flags and debug output

### 🐳 DevOps
- Multi-stage Dockerfile (Go core + Python runtime)

## [v0.2.0] - 2025-12-24
### 🚀 Added
- Template-driven scanning engine (Nuclei-like YAML templates).
- Template scan runner orchestrating core → matcher flow.
- Flexible matcher system (status, word, regex, body/headers).
- Python CLI (`pywvs`) with `scan` command.
- JSON reporter with structured findings output.
- HTML reporter powered by Jinja2 templates.
- Example templates (reflected XSS).
- End-to-end scan pipeline (CLI → core → matchers → report).

### 🧰 Fixed
- Import errors and naming inconsistencies across runners and reporters.
- Template loader path resolution.
- Core runner integration stability.

## [v0.1.0] - 2025-11-09
### Added
- Initial Go core (`wvs-core`) for banner grabbing and fingerprinting.
- Python wrapper (`pywvs.core_runner`) to run core and parse JSONL output.
- Base scanner interface (`pywvs.modules.base.ScannerModule`).
- Example scanner adapters (`modules/xss.py`, `modules/sqli.py`).
- Example scripts (`examples/run_core.py`, `examples/run_modules_adapters.py`).

## [v0.0.1] - 2025-10-13
### 🚀 Added
- Initial project scaffold (`README`, `LICENSE`, `SECURITY`, `.gitignore`)
- Base directory structure (`core-go`, `pywvs`, `templates`, etc.)
- GitHub templates (`ISSUE_TEMPLATE`, `PULL_REQUEST_TEMPLATE`)
- Example targets (DVWA, JuiceShop)
- Basic CI workflow and Dockerfile (multi-stage)
- Go core placeholder (`main.go`)

### 🧰 Fixed
- Code formatting with `black` to pass `flake8`

---

> 🧱 This is the initial scaffold release (v0.0.1) for **Web Vulnerability Scanner**.
