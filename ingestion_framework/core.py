from abc import ABC, abstractmethod
from typing import List, Dict

class SourceBase(ABC):
    """Interfaz base para cualquier fuente de datos (API, FTP, etc.)"""

    @abstractmethod
    def fetch_records(self, **kwargs) -> List[Dict]:
        pass

class StorageBase(ABC):
    """Interfaz base para cualquier storage (ADLS, S3, local, etc.)"""

    @abstractmethod
    def upload_record(self, record: Dict, file_name: str):
        pass

class StateManagerBase(ABC):
    """Interfaz base para manejo de estado incremental"""

    @abstractmethod
    def get_last_processed(self):
        pass

    @abstractmethod
    def update_last_processed(self, value):
        pass
