# ==========================================
# Name: BaseAPIClient
# Category: utils / api
# Description: Generic API client with retry, timeout and error handling
# ==========================================

import requests
import time
from typing import Optional, Dict


class BaseAPIClient:
    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict] = None,
        timeout: int = 10,
        max_retries: int = 3,
        backoff_factor: int = 2,
    ):
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"

        for attempt in range(self.max_retries):
            try:
                response = requests.request(
                    method,
                    url,
                    headers=self.headers,
                    timeout=self.timeout,
                    **kwargs,
                )

                if response.status_code == 200:
                    return response.json()

                elif response.status_code == 429:
                    wait = self.backoff_factor ** attempt
                    time.sleep(wait)

                elif response.status_code >= 500:
                    wait = self.backoff_factor ** attempt
                    time.sleep(wait)

                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text}")

            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(self.backoff_factor ** attempt)

        return None


    def get(self, endpoint: str, params: dict = None):
        return self._request("get", endpoint, params=params)

    def post(self, endpoint: str, data: dict = None):
        return self._request("post", endpoint, json=data)
