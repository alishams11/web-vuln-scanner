from scanner.form_finder import find_forms
from scanner.payload_injector import submit_form, is_vulnerable, XSS_PAYLOAD, SQLI_PAYLOAD

if __name__ == "__main__":
    url = input("Enter target URL: ").strip()
    forms = find_forms(url) 

    for form in forms:
        for payload, payload_type in [(XSS_PAYLOAD, "XSS"), (SQLI_PAYLOAD, "SQLi")]:
            response = submit_form(form, url, payload, payload_type)
            if is_vulnerable(response, payload):
                print(f"🔥 [VULNERABLE] {payload_type} vulnerability detected!")
            else:
                print(f"✅ [{payload_type}] Not vulnerable.")
