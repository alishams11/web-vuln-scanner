from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass
class TemplateRequest:
    method: str
    path: str
    payloads: Dict[str, List[str]]


@dataclass
class Matcher:
    type: str                     # word | regex | status | header
    part: str = "body"            # body | header | status
    words: Optional[List[str]] = None
    regex: Optional[List[str]] = None
    status: Optional[List[int]] = None


@dataclass
class Template:
    id: str
    name: str
    severity: str
    requests: List[TemplateRequest]
    matchers: List[Matcher]
