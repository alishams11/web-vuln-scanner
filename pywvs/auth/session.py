import requests
from .models import CredentialProfile


class AuthSession:
    

    def __init__(self, profile: CredentialProfile | None = None):
        self.session = requests.Session()
        self.profile = profile

        if profile:
            self._apply_profile(profile)

    def _apply_profile(self, profile: CredentialProfile):
        if profile.headers:
            self.session.headers.update(profile.headers)

        if profile.cookies:
            for k, v in profile.cookies.items():
                self.session.cookies.set(k, v)

    def request(self, method: str, url: str, **kwargs):
        return self.session.request(method, url, **kwargs)
