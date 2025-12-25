from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class APIRequest:
    method: str
    url: str
    headers: Dict[str, str]
    body: Optional[Any] = None   # dict (JSON) or raw str
