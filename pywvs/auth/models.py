from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class CredentialProfile:
    name: str
    type: str  # bearer | cookie | apikey | login
    headers: Optional[Dict[str, str]] = None
    cookies: Optional[Dict[str, str]] = None

    # login-flow
    login_url: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    username_field: Optional[str] = None
    password_field: Optional[str] = None
