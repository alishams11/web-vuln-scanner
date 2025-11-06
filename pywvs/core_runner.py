# pywvs/core_runner.py
import subprocess
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Generator, Optional


def run_wvs_core(urls: List[str], binary_path: str = "./wvs-core") -> Generator[Dict[str, Any], None, None]:
    """
    Run the Go core with a list of URLs.
    Yields: parsed JSON objects (one per response).
    Default binary_path points to ./wvs-core (built in repo root).
    """
    tmp_path = Path("/tmp/wvs_urls.txt")
    tmp_path.write_text("\n".join(urls))

    proc = subprocess.Popen(
        [binary_path, str(tmp_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if not proc.stdout:
        raise RuntimeError("wvs-core produced no stdout")

    # stream stdout line-by-line; each line is a JSON object
    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            # print warning to stderr but continue
            print(f"[WARN] invalid JSON from core (truncated): {line[:200]}", file=sys.stderr)

    # collect stderr and return code
    stderr = proc.stderr.read() if proc.stderr else ""
    ret = proc.wait()

    if ret != 0:
        raise RuntimeError(f"wvs-core exited with code {ret}\nSTDERR:\n{stderr}")

    if stderr:
        print(f"[wvs-core stderr]\n{stderr}", file=sys.stderr)


def run_wvs_core_from_file(urls_file: str, binary_path: str = "./wvs-core") -> List[Dict[str, Any]]:
    """
    Convenience: read URLs from a file and run the core.
    Returns list of response dicts.
    """
    p = Path(urls_file)
    if not p.exists():
        raise FileNotFoundError(f"{urls_file} not found")
    urls = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    return list(run_wvs_core(urls, binary_path=binary_path))


if __name__ == "__main__":
    # quick manual test: `python3 -m pywvs.core_runner`
    if len(sys.argv) > 1:
        out = run_wvs_core_from_file(sys.argv[1])
        print(json.dumps(out, indent=2))
    else:
        # example run
        out = list(run_wvs_core(["https://example.com", "https://httpbin.org/get"]))
        print(json.dumps(out, indent=2))
