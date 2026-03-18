# ==========================================
# Name: BaseAPIClient
# Category: utils / api
# Description: Generic API client with retry, timeout and error handling
# ==========================================

import requests
import time
from typing import Optional, Dict, Any


class APIRequestError(Exception):
    """Custom exception for API request failures"""
    pass


class BaseAPIClient:
    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
        max_retries: int = 3,
        backoff_factor: int = 2,
    ):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        url = self._build_url(endpoint)

        for attempt in range(self.max_retries):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    params=params,
                    json=data,
                    timeout=self.timeout,
                )

                # SUCCESS
                if response.status_code == 200:
                    return response.json()

                # RATE LIMIT
                elif response.status_code == 429:
                    wait_time = self.backoff_factor ** attempt
                    time.sleep(wait_time)

                # SERVER ERROR
                elif 500 <= response.status_code < 600:
                    wait_time = self.backoff_factor ** attempt
                    time.sleep(wait_time)

                # CLIENT ERROR
                else:
                    raise APIRequestError(
                        f"HTTP {response.status_code}: {response.text}"
                    )

            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise APIRequestError(str(e))
                time.sleep(self.backoff_factor ** attempt)

        raise APIRequestError("Max retries exceeded")

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("POST", endpoint, data=data)

    def set_headers(self, headers: Dict[str, str]):
        """Update headers dynamically (e.g., after authentication)"""
        self.headers.update(headers)

''' ----------------USE EXAMPLE----------------
client = BaseAPIClient(
    base_url="https://watermeter-api.grupoamper.com",
    timeout=10,
    max_retries=3,
)
'''
