from pathlib import Path
from typing import List


class IgnoreRule:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value


def load_ignore_file(path: Path) -> List[IgnoreRule]:
    rules = []

    if not path.exists():
        return rules

    for line in path.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        rules.append(IgnoreRule(key.strip(), value.strip()))

    return rules
