from ..core import SourceBase
from ..utils.retry import retry
import requests
from typing import List, Dict

class APIIngestion(SourceBase):
    def __init__(self, base_url, auth, logger=None):
        self.base_url = base_url
        self.auth = auth
        self.logger = logger

    def _build_headers(self):
        return self.auth.get_headers() if self.auth else {}

    @retry(retries=3, delay=2)
    def fetch_records(self, last_processed=None, endpoint="/data", params=None) -> List[Dict]:
        params = params or {}
        # ejemplo incremental
        if last_processed:
            params["updated_after"] = last_processed.isoformat()
        response = requests.get(f"{self.base_url}{endpoint}", headers=self._build_headers(), params=params)
        response.raise_for_status()
        return response.json().get("data", [])
