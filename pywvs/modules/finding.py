from dataclasses import dataclass
from typing import Dict


@dataclass
class Finding:
    rule_id: str
    name: str
    severity: str
    confidence: str  # high | medium | low
    url: str
    description: str
    evidence: Dict
