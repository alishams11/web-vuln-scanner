import requests
from urllib.parse import urljoin
from typing import Dict, Any, Optional

# simple payloads (you can expand)
XSS_PAYLOAD = "<script>alert('XSS')</script>"
SQLI_PAYLOAD = "' OR '1'='1"

REQUEST_TIMEOUT = 10
DEFAULT_HEADERS = {"User-Agent": "wvs-core/pywvs-adapter"}


def submit_form(form_details: Dict[str, Any], base_url: str, payload: str, vulnerable_type: str = "") -> Optional[requests.Response]:
    """
    Submit a form (form_details as returned by form_finder.get_form_details).
    Returns requests.Response or None on error.
    """
    try:
        target_url = urljoin(base_url, form_details.get("action", "") or "")
        data = {}

        for inp in form_details.get("inputs", []):
            name = inp.get("name")
            typ = (inp.get("type") or "text").lower()
            if not name:
                continue
            if typ in ("text", "search", "email", "url"):
                data[name] = payload
            elif typ in ("hidden", "value"):
                data[name] = inp.get("value", "")
            elif typ in ("submit",):
                # skip
                continue
            else:
                data[name] = "test"

        if form_details.get("method", "get").lower() == "post":
            return requests.post(target_url, data=data, timeout=REQUEST_TIMEOUT, headers=DEFAULT_HEADERS)
        else:
            return requests.get(target_url, params=data, timeout=REQUEST_TIMEOUT, headers=DEFAULT_HEADERS)
    except Exception:
        return None


def is_vulnerable(response: Optional[requests.Response], payload: str) -> bool:
    """
    Basic check: payload appears in response text.
    """
    if response is None:
        return False
    try:
        return payload in response.text
    except Exception:
        return False
