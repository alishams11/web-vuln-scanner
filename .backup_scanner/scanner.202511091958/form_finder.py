import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_all_forms(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.find_all("form")
    except Exception as e:
        print(f"[!] Error fetching forms: {e}")
        return []


def get_form_details(form):
    details = {}
    action = form.attrs.get("action", "").strip()
    method = form.attrs.get("method", "get").lower()
    inputs = []

    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})

    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def find_forms(url):
    forms = get_all_forms(url)
    results = []
    print(f"[+] Found {len(forms)} form(s) in {url}")
    for i, form in enumerate(forms, start=1):
        details = get_form_details(form)
        print(f"\n[#] Form #{i}")
        print(f"    Action: {details['action']}")
        print(f"    Method: {details['method']}")
        print("    Inputs:")
        for input_field in details["inputs"]:
            print(f"        - {input_field}")
        results.append(details)
    return results
