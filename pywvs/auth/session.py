import time
import requests
from typing import Optional

from .models import CredentialProfile


class AuthSession:
    """
    HTTP session with optional:
    - credential profile
    - polite mode (delay between requests)
    - custom User-Agent
    - proxy support
    """

    def __init__(
        self,
        profile: Optional[CredentialProfile] = None,
        polite: bool = False,
        user_agent: Optional[str] = None,
        proxy: Optional[str] = None,
        delay: float = 1.0,
    ):
        self.session = requests.Session()
        self.profile = profile
        self.polite = polite
        self.delay = delay

        # apply credential profile
        if profile:
            self._apply_profile(profile)

        # custom User-Agent
        if user_agent:
            self.session.headers["User-Agent"] = user_agent

        # proxy support
        if proxy:
            self.session.proxies.update(
                {
                    "http": proxy,
                    "https": proxy,
                }
            )

    def _apply_profile(self, profile: CredentialProfile):
        if profile.headers:
            self.session.headers.update(profile.headers)

        if profile.cookies:
            for k, v in profile.cookies.items():
                self.session.cookies.set(k, v)

    def request(self, method: str, url: str, **kwargs):
        if self.polite:
            time.sleep(self.delay)

        return self.session.request(method, url, **kwargs)
