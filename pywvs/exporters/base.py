from abc import ABC, abstractmethod
from typing import List
from pywvs.modules.base import Finding


class BaseExporter(ABC):
    @abstractmethod
    def export(self, findings: List[Finding], output_path: str) -> None:
        pass
