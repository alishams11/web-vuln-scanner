import subprocess
import json
from pathlib import Path


def test_cli_scan_creates_report(tmp_path):
    out = tmp_path / "report.json"

    subprocess.run(
        [
            "python3",
            "-m",
            "pywvs",
            "scan",
            "https://example.com",
            "-t",
            "pywvs/templates/xss-reflected.yaml",
            "-o",
            str(out),
        ],
        check=True,
    )

    assert out.exists()

    data = json.loads(out.read_text())
    assert isinstance(data, list)
