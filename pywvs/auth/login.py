from .models import CredentialProfile
import requests


def perform_login(profile: CredentialProfile) -> requests.Session:
    if not profile.login_url:
        raise ValueError("login_url is required")

    session = requests.Session()
    payload = {
        profile.username_field: profile.username,
        profile.password_field: profile.password,
    }

    resp = session.post(profile.login_url, data=payload, allow_redirects=True)

    if resp.status_code not in (200, 302):
        raise RuntimeError("Login failed")

    return session
