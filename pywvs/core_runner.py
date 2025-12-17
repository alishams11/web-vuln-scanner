import subprocess
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Generator


class CoreRunner:
    def __init__(self, binary_path: str = "./wvs-core"):
        self.binary_path = binary_path

    def run(self, urls: List[str]) -> Generator[Dict[str, Any], None, None]:
       
        if not urls:
            return
        
        tmp_path = Path("/tmp/wvs_urls.txt")
        tmp_path.write_text("\n".join(urls))

        proc = subprocess.Popen(
            [self.binary_path, str(tmp_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if not proc.stdout:
            raise RuntimeError("wvs-core produced no stdout")

        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                print(
                    f"[WARN] invalid JSON from core (truncated): {line[:200]}",
                    file=sys.stderr,
                )

        stderr = proc.stderr.read() if proc.stderr else ""
        ret = proc.wait()

        if ret != 0:
            raise RuntimeError(
                f"wvs-core exited with code {ret}\nSTDERR:\n{stderr}"
            )

        if stderr:
            print(f"[wvs-core stderr]\n{stderr}", file=sys.stderr)