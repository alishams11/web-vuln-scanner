import json
from .models import APIRequest


def load_api_request(path: str) -> APIRequest:
    """
    Expected JSON:
    {
      "method": "POST",
      "url": "https://api.example.com/login",
      "headers": {...},
      "body": {...}
    }
    """
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    return APIRequest(
        method=raw["method"],
        url=raw["url"],
        headers=raw.get("headers", {}),
        body=raw.get("body"),
    )
