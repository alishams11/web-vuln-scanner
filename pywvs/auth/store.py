import json
from pathlib import Path
from .models import CredentialProfile

BASE_DIR = Path.home() / ".web-vuln-scanner" / "credentials"
BASE_DIR.mkdir(parents=True, exist_ok=True)


def save_profile(profile: CredentialProfile):
    path = BASE_DIR / f"{profile.name}.json"
    with open(path, "w") as f:
        json.dump(profile.__dict__, f, indent=2)


def load_profile(name: str) -> CredentialProfile:
    path = BASE_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Credential profile '{name}' not found")

    data = json.loads(path.read_text())
    return CredentialProfile(**data)
