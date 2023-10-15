from abc import ABC, abstractmethod
from typing import Dict, Optional


class DataExtractorStrategy(ABC):
    """Base strategy class for data extraction."""

    @abstractmethod
    def extract_data(self, text: str) -> Dict[str, Optional[str]]:
        pass
