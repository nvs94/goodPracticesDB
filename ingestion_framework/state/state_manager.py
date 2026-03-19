from ..core import StateManagerBase
import os
from datetime import datetime

class FileStateManager(StateManagerBase):
    """Estado persistido en fichero"""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_last_processed(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return datetime.fromisoformat(f.read().strip())
        return None

    def update_last_processed(self, value: datetime):
        with open(self.file_path, "w") as f:
            f.write(value.isoformat())
