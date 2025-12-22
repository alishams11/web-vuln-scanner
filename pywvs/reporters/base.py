from abc import ABC, abstractmethod
from typing import List
from pywvs.modules.base import Finding


class Reporter(ABC):
    @abstractmethod
    def generate(self, findings: List[Finding], output_path: str) -> None:
        pass
