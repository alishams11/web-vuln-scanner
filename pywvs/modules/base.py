# pywvs/modules/base.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Finding:
    id: str
    name: str
    target: str
    severity: str  # e.g., "low", "medium", "high", "critical"
    confidence: float  # 0.0 - 1.0
    evidence: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class ScannerModule:
    """
    Base class for scanner modules.

    Subclasses should implement scan(target: str, core_results: List[Dict]) -> List[Finding].

    - target: the original target string (e.g., "https://example.com")
    - core_results: list of dicts produced by wvs-core for that target (or list of multiple responses)
    """

    name: str = "base"
    description: str = "Base scanner module"
    severity_default: str = "low"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    def scan(self, target: str, core_results: List[Dict[str, Any]]) -> List[Finding]:
        """
        Analyze core_results and return a list of Finding objects.

        Must be implemented by subclasses.
        """
        raise NotImplementedError("scan() must be implemented by module subclasses")
