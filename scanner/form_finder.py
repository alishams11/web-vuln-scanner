import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Dict, Any

REQUEST_TIMEOUT = 10


def get_all_forms(url: str) -> List:
    """
    Return list of BeautifulSoup form tags (raw).
    """
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
        soup = BeautifulSoup(resp.content, "html.parser")
        return soup.find_all("form")
    except Exception:
        return []


def get_form_details(form) -> Dict[str, Any]:
    """
    Normalize a BeautifulSoup <form> tag to a dict:
    {
      "action": "...",
      "method": "get|post",
      "inputs": [{"type": "...", "name": "..."}, ...]
    }
    """
    details: Dict[str, Any] = {}
    action = form.attrs.get("action", "").strip()
    method = form.attrs.get("method", "get").lower()
    inputs = []

    for input_tag in form.find_all(["input", "textarea", "select"]):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})

    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def find_forms(url: str) -> List[Dict[str, Any]]:
    """
    Return list of dicts (form details) for given url.
    This function is non-interactive (no printing).
    """
    forms = []
    raw_forms = get_all_forms(url)
    for f in raw_forms:
        try:
            forms.append(get_form_details(f))
        except Exception:
            # best-effort: skip broken forms
            continue
    return forms
