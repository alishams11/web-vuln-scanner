# 🧠 IPC Contract — Go ⇄ Python

This document defines the **Inter-Process Communication (IPC) contract** between the Go core engine (`wvs-core`) and the Python wrapper (`pywvs`).

The Go binary scans target URLs and returns structured results as **JSON**.

---

## 🧩 Output JSON Schema (Go → Python)

Each scan run produces a JSON array of **response objects**.

```json
[
  {
    "url": "https://example.com/login",
    "method": "GET",
    "status": 200,
    "headers": {
      "content-type": "text/html; charset=UTF-8",
      "server": "nginx"
    },
    "body_snippet": "<html>...</html>",
    "duration_ms": 153,
    "timestamp": "2025-10-13T12:30:00Z"
  }
]

---

## 🧾 Field Descriptions
Field	Type	Description
url	string	The target URL requested
method	string	HTTP method used (e.g., GET, POST)
status	integer	HTTP response status code
headers	object	Key/value pairs of response headers
body_snippet	string	First ~1KB of the response body (for analysis)
duration_ms	integer	Time taken for the request in milliseconds
timestamp	string (RFC3339)	When this request was executed

---
##🖥️ Example CLI usage
Go core:./wvs-core -target https://example.com -json > results.json

Python wrapper:
from pywvs import core
results = core.run_scan("https://example.com")
print(results[0]["status"], results[0]["url"])

---
##🔄 IPC Behavior
Communication: JSON is sent via stdout (Go → Python) and read as a stream.

Error Handling: Errors are written to stderr with an exit code ≠ 0.

Python Side Validation: Python verifies JSON conforms to schema using pydantic

---
📘 Document version: v0.1.0
📅 Date: 2025-10-13

---
