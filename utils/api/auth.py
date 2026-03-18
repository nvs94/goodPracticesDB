# ==========================================
# Name: BearerTokenManager
# Category: utils / api / auth
# Description: Handles token retrieval, caching and automatic refresh
# ==========================================

import time
from typing import Callable


class AuthenticationError(Exception):
    pass


class BearerTokenManager:
    def __init__(
        self,
        get_token_fn: Callable[[], dict],
        token_key: str = "token",
        expires_in_key: str = "expires_in",
        safety_margin: int = 60,
    ):
        """
        Args:
            get_token_fn: Function that retrieves a new token (must return dict)
            token_key: Key where token is stored in response
            expires_in_key: Key for token expiration (seconds)
            safety_margin: Seconds before expiration to refresh token
        """
        self.get_token_fn = get_token_fn
        self.token_key = token_key
        self.expires_in_key = expires_in_key
        self.safety_margin = safety_margin

        self._token = None
        self._expires_at = 0

    def _is_token_valid(self) -> bool:
        return self._token is not None and time.time() < self._expires_at

    def _refresh_token(self):
        response = self.get_token_fn()

        if not response or self.token_key not in response:
            raise AuthenticationError("Failed to retrieve token")

        self._token = response[self.token_key]

        # If API provides expiration
        expires_in = response.get(self.expires_in_key, 3600)
        self._expires_at = time.time() + expires_in - self.safety_margin

    def get_token(self) -> str:
        if not self._is_token_valid():
            self._refresh_token()
        return self._token
        
''' ----------------USE EXAMPLE----------------
client = BaseAPIClient(
    base_url="https://watermeter-api.grupoamper.com",
    timeout=10,
    max_retries=3,
)
'''
