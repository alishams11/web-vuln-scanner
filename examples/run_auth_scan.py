from pywvs.auth.store import load_profile
from pywvs.auth.session import AuthSession

profile = load_profile("dvwa")
session = AuthSession(profile)

resp = session.request("GET", "http://localhost/vulnerable.php")
print(resp.status_code)
