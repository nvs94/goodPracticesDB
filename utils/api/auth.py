import requests
from typing import Dict


class AuthBase:
    """Interfaz base de autenticación"""

    def get_headers(self) -> Dict[str, str]:
        raise NotImplementedError


class ApiKeyAuth(AuthBase):
    """Autenticación por API Key"""

    def __init__(self, api_key: str, header_name: str = "Authorization"):
        self.api_key = api_key
        self.header_name = header_name

    def get_headers(self):
        return {self.header_name: self.api_key}


class BearerTokenAuth(AuthBase):
    """Autenticación con token Bearer estático"""

    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {"Authorization": f"Bearer {self.token}"}


class OAuthClientCredentials(AuthBase):
    """
    OAuth2 Client Credentials flow
    """

    def __init__(self, token_url, client_id, client_secret, scope=None):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self._token = None

    def _fetch_token(self):
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        if self.scope:
            data["scope"] = self.scope

        response = requests.post(self.token_url, data=data)
        response.raise_for_status()

        self._token = response.json()["access_token"]

    def get_headers(self):
        if not self._token:
            self._fetch_token()

        return {"Authorization": f"Bearer {self._token}"}
