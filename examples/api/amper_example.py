# ==========================================
# Example: Amper API usage with Auth + Client
# ==========================================

from utils.api.base_client import BaseAPIClient
from utils.api.auth import BearerTokenManager

# ------------------------------------------
# CONFIG (esto vendrá de secrets en real)
# ------------------------------------------

BASE_URL = "https://watermeter-api.grupoamper.com"
USERNAME = "your_user"
PASSWORD = "your_password"

# ------------------------------------------
# STEP 1 — Create base client
# ------------------------------------------

client = BaseAPIClient(
    base_url=BASE_URL,
    timeout=10,
    max_retries=3,
)

# ------------------------------------------
# STEP 2 — Define login function
# ------------------------------------------

def amper_login():
    """
    Function used by the token manager to retrieve a new token
    """
    return client.post(
        "/admin/login",
        data={
            "username": USERNAME,
            "password": PASSWORD,
        },
    )

# ------------------------------------------
# STEP 3 — Create token manager
# ------------------------------------------

token_manager = BearerTokenManager(
    get_token_fn=amper_login
)

# ------------------------------------------
# STEP 4 — Helper to inject token
# ------------------------------------------

def get_authenticated_headers():
    token = token_manager.get_token()
    return {
        "Authorization": f"Bearer {token}"
    }

# ------------------------------------------
# STEP 5 — Example API call
# ------------------------------------------

def get_devices(limit: int = 1000):
    """
    Example function to retrieve devices
    """

    headers = get_authenticated_headers()

    client.set_headers(headers)

    response = client.get(
        "/device",
        params={"_limit": limit}
    )

    return response.get("items", [])


# ------------------------------------------
# RUN EXAMPLE
# ------------------------------------------

if __name__ == "__main__":

    devices = get_devices(limit=100)

    print(f"Retrieved {len(devices)} devices")
