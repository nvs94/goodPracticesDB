from datetime import datetime
from typing import Optional


class StateManager:
    """
    Interfaz base para gestión de estado (checkpoint).
    """

    def get_last_processed(self) -> Optional[datetime]:
        raise NotImplementedError

    def update_last_processed(self, value: datetime):
        raise NotImplementedError


class InMemoryStateManager(StateManager):
    """
    Implementación simple (testing / local)
    """

    def __init__(self):
        self._value = None

    def get_last_processed(self):
        return self._value

    def update_last_processed(self, value: datetime):
        self._value = value


class FileStateManager(StateManager):
    """
    Persistencia en fichero (simple y portable)
    """

    def __init__(self, filepath: str):
        self.filepath = filepath

    def get_last_processed(self):
        try:
            with open(self.filepath, "r") as f:
                value = f.read().strip()
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except:
            return None

    def update_last_processed(self, value: datetime):
        with open(self.filepath, "w") as f:
            f.write(value.strftime("%Y-%m-%d %H:%M:%S"))
