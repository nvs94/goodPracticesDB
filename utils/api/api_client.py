import requests
import logging
from typing import Dict, Optional
from retry import retry


class APIClient:
    """
    Cliente HTTP reutilizable.
    """

    def __init__(
        self,
        base_url: str,
        auth=None,
        default_headers: Optional[Dict] = None,
        timeout: int = 30,
        logger: Optional[logging.Logger] = None,
    ):
        self.base_url = base_url
        self.auth = auth
        self.default_headers = default_headers or {}
        self.timeout = timeout
        self.logger = logger or logging.getLogger(__name__)

    def _build_headers(self):
        headers = self.default_headers.copy()

        if self.auth:
            headers.update(self.auth.get_headers())

        return headers

    @retry(retries=3, delay=2)
    def get(self, endpoint: str, params: Dict = None):
        url = f"{self.base_url}{endpoint}"

        response = requests.get(
            url,
            headers=self._build_headers(),
            params=params,
            timeout=self.timeout,
        )

        response.raise_for_status()

        self.logger.info(f"GET {url} - {response.status_code}")
        return response.json()

    @retry(retries=3, delay=2)
    def post(self, endpoint: str, json: Dict = None):
        url = f"{self.base_url}{endpoint}"

        response = requests.post(
            url,
            headers=self._build_headers(),
            json=json,
            timeout=self.timeout,
        )

        response.raise_for_status()

        self.logger.info(f"POST {url} - {response.status_code}")
        return response.json()
